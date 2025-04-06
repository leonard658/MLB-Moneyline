
import re
import numpy as np
import pandas as pd


def groupsOf3Aggregate(df: pd.DataFrame) -> pd.DataFrame:
    def aggregate_lineup_features(df: pd.DataFrame, var_threshold: float = 1e-5) -> pd.DataFrame:
        """
        Aggregates batting lineup features into three groups for positions 1-3, 4-6, and 7-9.
        For each group, the function computes a row-wise mean and standard deviation while ignoring NaN values.
        If the overall standard deviation of the aggregated feature (across all rows)
        is below var_threshold, then the aggregated features are dropped.
        
        Parameters:
        df: pandas DataFrame containing individual player stats (e.g., "woba_2_home").
        var_threshold: Features with overall std (across rows) below this threshold are dropped.
                        Default is 1e-5.
        
        Returns:
        A DataFrame with new aggregated features replacing the original individual columns for each group.
        """
        # Work on a copy of the DataFrame to avoid modifying the original.
        new_df = df.copy()
        
        # Dictionary to group columns by (stat_prefix, team, group)
        grouped_cols = {}  # key: (stat_prefix, team, group), value: list of column names
        
        # Regular expression to capture columns like "woba_2_home"
        pattern = re.compile(r'^(.*?)_(\d+)_((?:home)|(?:away))$')
        
        # Loop over each column to group them by stat, team, and batting order group.
        for col in new_df.columns:
            m = pattern.match(col)
            if m:
                stat_prefix = m.group(1)
                pos = int(m.group(2))
                team = m.group(3)
                # Only consider positions 1-9
                if 1 <= pos <= 9:
                    # Group 1: positions 1-3, Group 2: positions 4-6, Group 3: positions 7-9
                    if pos <= 3:
                        group = 1
                    elif pos <= 6:
                        group = 2
                    else:
                        group = 3
                    key = (stat_prefix, team, group)
                    if key not in grouped_cols:
                        grouped_cols[key] = []
                    grouped_cols[key].append(col)
        
        # Process each group to compute aggregated features.
        for key, col_list in grouped_cols.items():
            stat_prefix, team, group = key
            # Convert the group's columns to a NumPy array.
            subset = new_df[col_list].to_numpy()
            
            # Compute the row-wise mean and standard deviation ignoring NaN values.
            group_mean = np.nanmean(subset, axis=1)
            group_std = np.nanstd(subset, axis=1)
            
            # Check overall variability of the aggregated mean.
            overall_std = np.nanstd(group_mean)
            
            # Define new column names for aggregated features.
            mean_col_name = f"{stat_prefix}_group{group}_{team}"
            std_col_name = f"{stat_prefix}_group{group}_{team}_std"
            
            # Only add aggregated features if the overall variability meets the threshold.
            if overall_std >= var_threshold:
                new_df[mean_col_name] = group_mean
                new_df[std_col_name] = group_std
            
            # Drop the original individual columns.
            for col in col_list:
                if col in new_df.columns:
                    new_df.drop(columns=col, inplace=True)
        return new_df

    df = df.drop(labels = ["date", "total_bullpen_home", "total_bullpen_away"], axis = 'columns')
    return aggregate_lineup_features(df, var_threshold=0)

def groupOf9Aggregate(df: pd.DataFrame) -> pd.DataFrame:
    def aggregate_lineup_features(df: pd.DataFrame, var_threshold: float = 1e-5) -> pd.DataFrame:
        """
        Aggregates batting lineup features into one group (positions 1-9)
        for each stat and team. For each group, the function computes:
        - Mean
        - Standard Deviation
        
        NaN values are ignored in all calculations.
        The original individual columns for each group are then dropped.
        
        Parameters:
        df: pandas DataFrame containing individual player stats (e.g., "woba_2_home").
        var_threshold: Features with overall std (across rows) below this threshold are dropped.
                        Default is 1e-5.
        
        Returns:
        A DataFrame with new aggregated features replacing the original per-player columns.
        """
        # Drop non-numeric columns that aren't needed.
        for col in ["date", "total_bullpen_home", "total_bullpen_away"]:
            if col in df.columns:
                df = df.drop(columns=col)
        
        new_df = df.copy()
        
        # Group columns by (stat_prefix, team) for positions 1-9.
        grouped_cols = {}  # key: (stat_prefix, team), value: list of column names
        pattern = re.compile(r'^(.*?)_(\d+)_((?:home)|(?:away))$')
        
        for col in new_df.columns:
            m = pattern.match(col)
            if m:
                stat_prefix = m.group(1)
                pos = int(m.group(2))
                team = m.group(3)
                if 1 <= pos <= 9:
                    key = (stat_prefix, team)
                    if key not in grouped_cols:
                        grouped_cols[key] = []
                    grouped_cols[key].append(col)
        
        # Process each group to compute aggregated features.
        for key, col_list in grouped_cols.items():
            stat_prefix, team = key
            
            # Convert the group's columns to a NumPy array.
            subset = new_df[col_list].to_numpy()
            
            # Compute the row-wise mean and standard deviation ignoring NaN values.
            group_mean = np.nanmean(subset, axis=1)
            group_std  = np.nanstd(subset, axis=1)
            
            # Check overall variability of the aggregated mean.
            overall_std = np.nanstd(group_mean)
            
            # Define new column names for the aggregated features.
            mean_col_name = f"{stat_prefix}_{team}_all_mean"
            std_col_name  = f"{stat_prefix}_{team}_all_std"
            
            # Only add aggregated features if the overall variability meets the threshold.
            if overall_std >= var_threshold:
                new_df[mean_col_name] = group_mean
                new_df[std_col_name]  = group_std
            
            # Drop the original individual columns for this group.
            for col in col_list:
                if col in new_df.columns:
                    new_df.drop(columns=col, inplace=True)
        
        return new_df
    df = df.drop(labels = ["date", "total_bullpen_home", "total_bullpen_away"], axis = 'columns')
    return aggregate_lineup_features(df, var_threshold=0)


def noFeatureEngineering(df: pd.DataFrame) -> pd.DataFrame:
    irrelevant_stats = [
    "date", 
    "gamePk", 
    "total_1_home", 
    "pitch_percentage_1_home", 
    "total_vs_hand_1_home", 
    "pitch_percentage_vs_hand_1_home", 
    "total_2_home", 
    "pitch_percentage_2_home", 
    "total_vs_hand_2_home", 
    "pitch_percentage_vs_hand_2_home", 
    "total_3_home", 
    "pitch_percentage_3_home", 
    "total_vs_hand_3_home", 
    "pitch_percentage_vs_hand_3_home", 
    "total_4_home", 
    "pitch_percentage_4_home", 
    "total_vs_hand_4_home", 
    "pitch_percentage_vs_hand_4_home", 
    "total_5_home", 
    "pitch_percentage_5_home", 
    "total_vs_hand_5_home", 
    "pitch_percentage_vs_hand_5_home", 
    "total_6_home", 
    "pitch_percentage_6_home", 
    "total_vs_hand_6_home", 
    "pitch_percentage_vs_hand_6_home", 
    "total_7_home", 
    "pitch_percentage_7_home", 
    "total_vs_hand_7_home", 
    "pitch_percentage_vs_hand_7_home", 
    "total_8_home", 
    "pitch_percentage_8_home", 
    "total_vs_hand_8_home", 
    "pitch_percentage_vs_hand_8_home", 
    "total_9_home", 
    "pitch_percentage_9_home", 
    "total_vs_hand_9_home", 
    "pitch_percentage_vs_hand_9_home", 
    "total_pitch_home", 
    "pitch_percentage_pitch_home", 
    "total_pitch_home_1", 
    "pitch_percentage_pitch_home_1", 
    "total_bullpen_home", 
    "pitch_percentage_bullpen_home", 
    "total_1_away", 
    "pitch_percentage_1_away", 
    "total_vs_hand_1_away", 
    "pitch_percentage_vs_hand_1_away", 
    "total_2_away", 
    "pitch_percentage_2_away", 
    "total_vs_hand_2_away", 
    "pitch_percentage_vs_hand_2_away", 
    "total_3_away", 
    "pitch_percentage_3_away", 
    "total_vs_hand_3_away", 
    "pitch_percentage_vs_hand_3_away", 
    "total_4_away", 
    "pitch_percentage_4_away", 
    "total_vs_hand_4_away", 
    "pitch_percentage_vs_hand_4_away", 
    "total_5_away", 
    "pitch_percentage_5_away", 
    "total_vs_hand_5_away", 
    "pitch_percentage_vs_hand_5_away", 
    "total_6_away", 
    "pitch_percentage_6_away", 
    "total_vs_hand_6_away", 
    "pitch_percentage_vs_hand_6_away", 
    "total_7_away", 
    "pitch_percentage_7_away", 
    "total_vs_hand_7_away", 
    "pitch_percentage_vs_hand_7_away", 
    "total_8_away", 
    "pitch_percentage_8_away", 
    "total_vs_hand_8_away", 
    "pitch_percentage_vs_hand_8_away", 
    "total_9_away", 
    "pitch_percentage_9_away", 
    "total_vs_hand_9_away", 
    "pitch_percentage_vs_hand_9_away", 
    "total_pitch_away", 
    "pitch_percentage_pitch_away", 
    "total_pitch_away_1", 
    "pitch_percentage_pitch_away_1", 
    "total_bullpen_away", 
    "pitch_percentage_bullpen_away"
    ]
    return df.drop(labels = irrelevant_stats, axis = 'columns')


    