import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from datetime import datetime

# Step 3: Load and Preprocess the Data
# Load the dataset
data = pd.read_csv('procrastination_data.csv')

# Convert time columns to datetime
time_columns = ['TaskStartTime', 'TaskEndTime', 'Deadline', 'SubmissionTime']
for col in time_columns:
    data[col] = pd.to_datetime(data[col])

# Calculate task duration and delay
data['TaskDuration'] = (data['TaskEndTime'] - data['TaskStartTime']).dt.total_seconds() / 60
data['Delay'] = (data['SubmissionTime'] - data['Deadline']).dt.total_seconds() / 60

# Display the processed data
print("Processed Data:")
print(data.head())

# Step 4: Analyze Procrastination Patterns
# Calculate average distraction duration and delay per user
user_stats = data.groupby('UserID').agg({
    'DistractionDuration': 'mean',
    'Delay': 'mean'
}).reset_index()

# Rename columns for clarity
user_stats.rename(columns={
    'DistractionDuration': 'AvgDistractionDuration',
    'Delay': 'AvgDelay'
}, inplace=True)

# Display user statistics
print("\nUser Statistics:")
print(user_stats)

# Step 5: Visualize Procrastination Patterns
# Plot average distraction duration vs. average delay
plt.figure(figsize=(10, 6))
plt.scatter(user_stats['AvgDistractionDuration'], user_stats['AvgDelay'], c='blue', alpha=0.7)
plt.title('Procrastination Patterns: Distraction vs. Delay')
plt.xlabel('Average Distraction Duration (minutes)')
plt.ylabel('Average Delay (minutes)')
plt.grid(True)
plt.show()

# Step 6: Clustering Users Based on Procrastination Behavior
# Prepare data for clustering
X = user_stats[['AvgDistracti

onDuration', 'AvgDelay']]

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
user_stats['Cluster'] = kmeans.fit_predict(X)

# Display clustered user statistics
print("\nClustered User Statistics:")
print(user_stats)

# Visualize clusters
plt.figure(figsize=(10, 6))
for cluster in user_stats['Cluster'].unique():
    cluster_data = user_stats[user_stats['Cluster'] == cluster]
    plt.scatter(cluster_data['AvgDistractionDuration'], cluster_data['AvgDelay'], label=f'Cluster {cluster}')
plt.title('User Clusters Based on Procrastination Behavior')
plt.xlabel('Average Distraction Duration (minutes)')
plt.ylabel('Average Delay (minutes)')
plt.legend()
plt.grid(True)
plt.show()

Data set 
UserID  TaskID        TaskStartTime          TaskEndTime  DistractionDuration            Deadline       SubmissionTime  TaskDuration  Delay
0       1     101 2023-10-01 10:00:00 2023-10-01 12:00:00                  30 2023-10-01 18:00:00 2023-10-01 17:55:00         120.0   -5.0
1       1     102 2023-10-02 09:00:00 2023-10-02 11:00:00                 120 2023-10-02 18:00:00 2023-10-02 17:50:00         120.0  -10.0
2       2     103 2023-10-01 14:00:00 2023-10-01 16:00:00                  60 2023-10-01 18:00:00 2023-10-01 18:30:00         120.0   30.0
3       2     104 2023-10-02 10:00:00 2023-10-02 12:00:00                  90 2023-10-02 18:00:00 2023-10-02 18:15:00         120.0   15.0
