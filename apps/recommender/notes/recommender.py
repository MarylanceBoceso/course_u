from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User


from django.shortcuts import get_object_or_404

from django.utils.safestring import mark_safe

from .models import UserSkill, UserSkillSource, UserRecommendations

from apps.website.models import Skill, Specialization, SpecializationSkills, Field, LearningMaterial
from apps.acad.models import StudentProfile

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

import os
import plotly.express as px
import plotly.io as pio


def recommender(request):
    # Get the user's skills from the request.
    user_skills = UserSkill.objects.filter(user=request.user)
    user_skills_list = [skill.skill.skill for skill in user_skills]
    user_skills_list = list(set(user_skills_list))
    user_skills_list = list(user_skills_list)

    normalized_field_skills = load_csv(request)

    normalized_user_skills_df_columns = user_skills_list
    
    normalized_field_skills_columns = normalized_field_skills.columns
    # convert to list
    normalized_field_skills_columns = list(normalized_field_skills_columns)
    #intersection_columns = normalized_user_skills_df_columns.intersection(normalized_field_skills_columns)
    intersection_columns = set(normalized_user_skills_df_columns).intersection(set(normalized_field_skills_columns))


    # to list for filtering
    intersection_columns = list(intersection_columns)
    print("Len of interseciotn columns: ", len(intersection_columns))
    #print('intersection_columns: ', intersection_columns)

    if len(intersection_columns) == 0:
        return render(request, 'recommender/recommender_failed.html')


    # get level of each skill
    user_skills_level = []
    for skill in intersection_columns:
        userskill_level = UserSkill.objects.get(user=request.user, skill__skill=skill).level
        user_skills_level.append(userskill_level)


    user_skills_dict = dict(zip(intersection_columns, user_skills_level))   
    user_skills_df = pd.DataFrame.from_dict(user_skills_dict, orient='index').T

    # use tfidf
    tfidf = TfidfTransformer()
    normalized_user_skills_df = pd.DataFrame(tfidf.fit_transform(user_skills_df).toarray(), columns=user_skills_df.columns, index=user_skills_df.index)

    # Filter the specialization data frame columns by the user's skills. except the first and second columns
    normalized_field_skills_filtered = normalized_field_skills[['field_id'] + intersection_columns]
    normalized_field_skills_filtered = normalized_field_skills_filtered[(normalized_field_skills_filtered[intersection_columns] != 0).any(axis=1)]


    cosine_similarities = cosine_similarity(normalized_user_skills_df[intersection_columns], normalized_field_skills_filtered[intersection_columns])
    #print('cosine_similarities: ', cosine_similarities)
    top_3_indices = cosine_similarities.argsort(axis=1)[:, -3:]
    top_3_field = normalized_field_skills_filtered.iloc[:, 0].values[top_3_indices]
    all_fields = normalized_field_skills_filtered.iloc[:, 0].values
 
    field_ids = normalized_field_skills_filtered['field_id'].unique()
    # Create a dictionary to store the field names and the sum of the cosine similarity scores
    fields_score = {}
    for field_id in all_fields:
        normalized_field_skills_filtered_by_field = normalized_field_skills_filtered[normalized_field_skills_filtered['field_id'] == field_id]
        fields_score[field_id] = normalized_field_skills_filtered_by_field.iloc[:, 1:].sum(axis=1).sum()
    
    # get field names
    fields_name = []
    for field_id in all_fields:
        field_name = Field.objects.get(field=field_id).field_name
        fields_name.append(field_name)

    field_dict = {
        'Software Development': 1,
        'Data and Analytics': 2,
        'Design and UX/UI': 3,
        'Product Management': 4,
        'Testing and Quality Assurance': 5,
        'Security': 6
    }
    field_dict = {v: k for k, v in field_dict.items()}


    # Calculate the field with the highest matching for each skill
    user_skills_field = []
    field_id_list = []
    for skill in intersection_columns:
        field_id = normalized_field_skills_filtered.loc[normalized_field_skills_filtered[skill].idxmax(), 'field_id']
        field_id_list.append(field_id)
        field = Field.objects.get(field=field_id).field_name
        user_skills_field.append(field)
    
    user_skills_df = pd.DataFrame({
        'skill': intersection_columns,
        'level': user_skills_level,
        'field': user_skills_field,
        'field_id': field_id_list,
    })
    #pivot_df = user_skills_df.pivot(index='skill', columns='field', values='level').fillna(0)


    user_skills_df['fields_score'] = user_skills_df['field_id'].map(fields_score)
    user_skills_df = user_skills_df.sort_values('fields_score', ascending=False)
    user_skills_df = user_skills_df.drop('fields_score', axis=1)


    fig = px.bar(
        user_skills_df,
        x='level',
        y='field',
        barmode ='stack',
        hover_data=['skill'],
        orientation='h',
        labels={'level': 'Count', 'field': 'Field'},
        #color_discrete_sequence=list(field_dict.values()),
        color='field',
    )

    # x and y title
    #fig.update_xaxes(title_text='Skill Level')
    #fig.update_yaxes(title_text='Skill Name')
    fig.update_xaxes(title_text='Count')
    fig.update_yaxes(title_text='Field')
    skill_plot = pio.to_html(fig, full_html=False)

    # Create a DataFrame with Field_ID, Field_Name, and Score
    fields_df = pd.DataFrame(list(zip(field_ids, fields_name, fields_score.values())), columns=['Field_ID', 'Field_Name', 'Score'])
    print('fields_df: ', fields_df)
    # Create a pie chart using Plotly Express
    fig = px.pie(fields_df, values='Score', names='Field_Name',
                 #title='Top Field Recommendation Score'
                 )

    # set title
    #fig.update_layout(title_text='Top Field Recommendation Score', title_x=0.5)

    # remove white background
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    # Convert the figure to HTML
    field_plot = pio.to_html(fig, full_html=False)
    # make a copy of normamlied_field
    normalized_copy = normalized_field_skills_filtered.copy()
    # label field id of normalized_field_skills_filtered with field_dict
    normalized_copy['field_name'] = normalized_copy['field_id'].map(field_dict)
    # melt normalized_field_skills_filtered
    normalized_copy = normalized_copy.melt(id_vars=['field_id', 'field_name'], var_name='skill', value_name='level')
    # use fields_score mapping for field_id into field_order
    normalized_copy['field_order'] = normalized_copy['field_id'].map(fields_score)
    # sort by field_order
    normalized_copy = normalized_copy.sort_values('field_order', ascending=False)
    # remove field_order
    normalized_copy = normalized_copy.drop('field_order', axis=1)

    print('normalized_copy: ', normalized_copy)

    stacked_skills = px.bar(
        normalized_copy, 
        x='level', 
        y='field_name', 
        color='field_name', 
        # title='Skills Levels',
        orientation='h',
        labels={'level': 'Relevance Score',  'skill': 'Skill'}, #'field_name': 'Field Name',
        color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )

    # convert to html
    stacked_skills = pio.to_html(stacked_skills, full_html=False)

    # create the radar chart
    radar_skills = px.line_polar(
        normalized_copy, 
        r='level', 
        theta='skill', 
        color='field_name', 
        line_close=True,
        # title='Skills Levels',
        labels={'level': 'Relevance Score', 'field_name': 'Field Name'},
        #color_continuous_scale=px.colors.sequential.Plasma,
        height=500,
        width=800,
    )
    radar_skills = pio.to_html(radar_skills, full_html=False)

    # Sort the fields by the sum of the cosine similarity scores, in descending order.
    top_3_fields = sorted(fields_score, key=fields_score.get, reverse=True)[:3]
    top_3_fields_score = [fields_score[field_id] for field_id in top_3_fields]

    field_names = []
    for field_id in top_3_fields:
        field_name = Field.objects.get(field=field_id).field_name
        field_names.append(field_name)

    field_name_1 = field_names[0]
    field_name_2 = field_names[1]
    field_name_3 = field_names[2]

    # get StudentProfile year
    student_year = StudentProfile.objects.get(user=request.user).current_year

    #UserRecommendations get or create
    user_recommendations = UserRecommendations.objects.get_or_create(user=request.user, current_year=student_year)[0]

    user_recommendations.field_1 = Field.objects.get(field=top_3_fields[0])
    user_recommendations.field_2 = Field.objects.get(field=top_3_fields[1])
    user_recommendations.field_3 = Field.objects.get(field=top_3_fields[2])
    user_recommendations.score_1 = float(top_3_fields_score[0])
    user_recommendations.score_2 = float(top_3_fields_score[1])
    user_recommendations.score_3 = float(top_3_fields_score[2])


    user_recommendations.save()


    return render(request, 'recommender/recommender.html', {
        'top_3_field_recommendations': top_3_field,
        'field_name_1': field_name_1,
        'field_name_2': field_name_2,
        'field_name_3': field_name_3,
        'skill_plot': skill_plot,
        'field_plot': field_plot,
        'stacked_skills': stacked_skills,
        'radar_skills': radar_skills,
        'field_1': Field.objects.get(field=top_3_fields[0]),
        'field_2': Field.objects.get(field=top_3_fields[1]),
        'field_3': Field.objects.get(field=top_3_fields[2]),
    })