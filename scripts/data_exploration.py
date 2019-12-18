# -*- coding: utf-8 -*-

### Import libraries ###

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
sns.set_style("dark")
import os

### Functions ###

def most_reviewed_products(df, n_products):
    reviews_per_product = df['asin'].value_counts()
    most_reviews = reviews_per_product.nlargest(n_products)
    most_reviews = most_reviews.reset_index()
    most_reviews = most_reviews.drop('asin', axis=1)
    definitive = df.merge(most_reviews, left_on='asin', right_on='index')
    definitive = definitive.drop('index', axis=1)
    return definitive


def most_active_reviewers(df, n_reviewers):
    n_reviews = df['reviewerID'].value_counts()
    most_reviews = n_reviews.nlargest(n_reviewers)
    most_reviews = most_reviews.reset_index()
    most_reviews = most_reviews.drop('reviewerID', axis=1)
    definitive = df.merge(most_reviews, left_on='reviewerID', right_on='index')
    definitive = definitive.drop('index', axis=1)
    return definitive

def analyze_reviews(df, plot_title):
    print("Shape of df: ", df.shape)

    fig, ax1 = plt.subplots()
    sns.countplot(df.overall, ax=ax1)
    ax1.set_title(plot_title)
    #plt.show()
    # ax1.figure.savefig('figures/unverified_scoredistribution.svg', format='svg')
    # print("Exported unverified_scoredistribution.svg")

    print("Average Score: ", np.mean(df.overall))
    print("Median Score: ", np.median(df.overall))
#%%

def run(df):
    current_directory = os.getcwd()
    os.chdir('..')
    
    # Number of words for each review
    fig, ax = plt.subplots(figsize=(10,10))
    ax.boxplot(df['n_words'])
    ax.set_xlabel('Reviews')
    ax.figure.savefig('figures/1_lengthreviews.svg', format='svg')
    print('Exported 1_lengthreviews.svg')

    # Score Distribution
    fig, ax1 = plt.subplots()
    sns.countplot(df.overall, ax=ax1)
    ax1.set_title('Score Distribution')
    # plt.show()
    ax1.figure.savefig('figures/1_scoredistribution.svg', format='svg')
    print("Exported 1_scoredistribution.svg")

    #Opinion Distribution
    fig, ax2 = plt.subplots()
    sns.countplot(df.opinion, ax=ax2)
    ax2.set_title('Opinion Distribution')
    ax2.figure.savefig('figures/1_opiniondistribution.svg', format='svg')
    print("Exported 1_opiniondistribution.svg")

    #Stacked barplot (x-axis asin code, y-axis opinion)
    fig, ax3 = plt.subplots()
    top_products = most_reviewed_products(df, 20)
    r = list(top_products['asin'].unique())
    positive = list(top_products.loc[top_products['opinion'] == 'positive', 'asin'].value_counts().reindex(top_products['asin'].unique(), fill_value=0))
    neutral = list(top_products.loc[top_products['opinion'] == 'neutral', 'asin'].value_counts().reindex(top_products['asin'].unique(), fill_value=0))
    negative = list(top_products.loc[top_products['opinion'] == 'negative', 'asin'].value_counts().reindex(top_products['asin'].unique(), fill_value=0))
    raw_data = {'positive': positive, 'neutral': neutral, 'negative': negative}
    raw_data = pd.DataFrame(raw_data)

    #print("Opinions ",raw_data)
    
    totals = [i+j+k for i,j,k in zip(raw_data['positive'], raw_data['neutral'], raw_data['negative'])]
    #totals = list(top_products['asin'].value_counts().reindex(top_products['asin'].unique(), fill_value=0))
    positive_percentage = [i / j * 100 for i, j in zip(raw_data['positive'], totals)]
    neutral_percentage = [i / j * 100 for i, j in zip(raw_data['neutral'], totals)]
    negative_percentage = [i / j * 100 for i, j in zip(raw_data['negative'], totals)]

    bar_width = 0.85

    ax3.bar(r, positive_percentage, color='#b5ffb9', edgecolor='white', width=bar_width)
    ax3.bar(r, neutral_percentage, bottom=positive_percentage, color='#f9bc86', edgecolor='white', width=bar_width)
    ax3.bar(r, negative_percentage, bottom=[i + j for i, j in zip(positive_percentage, neutral_percentage)], color='#a3acff', edgecolor='white', width=bar_width)
    #ax.xticks(r, names, rotation=90)
    ax3.set_xticklabels(r, rotation=90)
    ax3.set_xlabel('Code product')
    # plt.show()
    ax3.figure.savefig('figures/1_reviews.svg', format='svg')
    print("Exported 1_reviews.svg")

    # Top 50 reviewers
    fig, ax4 = plt.subplots()
    top_reviewers = most_active_reviewers(df, 50)
    top_reviewers = top_reviewers.groupby('reviewerID').agg({'overall':'mean',
                                                             'vote':'mean',
                                                             'asin':'count'}).sort_values(['asin'], ascending=[False]).reset_index()

    r = list(top_reviewers['reviewerID'].unique())
    bar_width = 0.85

    ax4.bar(r, top_reviewers['asin'], color='#f9bc86', edgecolor='white', width=bar_width)
    ax4.bar(r, top_reviewers['overall'], color='#b5ffb9', edgecolor='white', width=bar_width)
    ax4.set_xticklabels(r, rotation=90)
    ax4.set_xlabel('Reviewer ID')
    ax4.figure.savefig('figures/1_reviewers.svg', format='svg')
    print("Exported 1_reviewers.svg")

    #Non verified reviews
    print("### Unverified reviews exploration ###")
    unverified = df[df['verified'] == False]
    analyze_reviews(unverified, "Unverified Score Distribution")

    unverified2 = unverified[unverified['opinion'] == 'negative']
    print("Negative unverified", unverified2.shape)
    unverified2_head = unverified2.head(10)['reviewText']
    for x in unverified2_head:
        print("Review: ", x)

    unverified3 = unverified[unverified['opinion'] == 'positive']
    print("Positive unverified", unverified3.shape)
    unverified3_head = unverified3.head(10)['reviewText']
    for x in unverified3_head:
        print("Review: ", x)

    fig, ax5 = plt.subplots(figsize=(10,10))
    ax5.boxplot(unverified['n_words'])
    ax5.set_xlabel('Unverified Reviews')
    #ax5.figure.savefig('figures/1_lengthunverifiedreviews.svg', format='svg')

    #Verified reviews
    print("### Verified reviews exploration ###")
    verified = df[df['verified'] == True]
    analyze_reviews(verified, "Verified Score Distribution")

    fig, ax6 = plt.subplots(figsize=(10,10))
    ax6.boxplot(verified['n_words'])
    ax6.set_xlabel('Verified Reviews')
    #ax5.figure.savefig('figures/1_lengthunverifiedreviews.svg', format='svg')

    plt.show()

    os.chdir(current_directory)