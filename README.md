# World Values Survey Data Visualization

This Streamlit application visualizes data from the World Values Survey, allowing users to explore trends and values across different countries and survey waves. The app displays average responses for selected survey questions over time, making it easier to investigate cultural and social value shifts.

## Features

- **Country and Wave Selection**: Choose from multiple countries and survey waves for analysis.
- **Question Selection**: View trends for selected questions, each visualized with line plots for easy comparison across countries.
- **Responsive Layout**: Enlarged graphs and a streamlined layout ensure clarity and accessibility.
- **Data Source and Citation**: The data source and authorship are acknowledged directly within the app.

## Requirements

To install required packages, run the following command in your terminal:

pip install -r requirements.txt

## Installation and Running the App

1. Clone the repository:

   git clone <repository-url>
   cd <repository-directory>

2. Run the app:

   streamlit run app.py

3. Open your browser and go to `http://localhost:8501` to view the app.

## Data Preparation

The application requires a precomputed dataset file named `precomputed_means.csv`, which should contain mean values of survey responses for different countries and waves. This CSV file must be placed in the app directory and should follow the format:

COUNTRY_ALPHA, S002VS, [question columns]

## Usage

- **Select Countries and Waves**: Choose the countries and survey waves you want to explore from the sidebar.
- **Choose Questions**: The app allows you to select multiple questions and generates separate visualizations for each.
- **Citation Information**: Located in the sidebar under filters for proper data acknowledgment.

## Citation

To cite the World Values Survey data used in this application, please refer to:

**WVS time-series (1981-2022):**  
Inglehart, R., Haerpfer, C., Moreno, A., Welzel, C., Kizilova, K., Diez-Medrano J., M. Lagos, P. Norris, E. Ponarin & B. Puranen (eds.). 2022. *World Values Survey: All Rounds – Country-Pooled Datafile Version 3.0*. Madrid, Spain & Vienna, Austria: JD Systems Institute & WVSA Secretariat. doi:10.14281/18241.17  

For more information, visit the [World Values Survey Documentation](https://www.worldvaluessurvey.org/WVSDocumentationWVL.jsp).

**Developer**: Jaronimas Snipas  
- [GitHub](https://github.com/jaronimas-codes)  
- [LinkedIn](https://www.linkedin.com/in/jaronimas-snipas/)
