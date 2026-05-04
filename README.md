# PyTCG-Eval: Automated Python Test Case Generation and Evaluation System

## Author
Binita Chourasia

## Project Description
PyTCG-Eval is a system designed to automatically generate and evaluate test cases for Python programs. In many real-world situations, writing test cases manually takes a lot of time and effort, and sometimes important scenarios are missed. This system solves that problem by providing a simple and structured way to create and test unit cases.

The system takes Python source code as input, either from local files or a GitHub repository. It then uses different open-source tools to generate unit tests automatically. After that, it runs those tests and checks how effective they are by using coverage metrics such as line coverage, branch coverage, and mutation coverage. The results are shown in a dashboard so that users can clearly understand how well their code is tested. :contentReference[oaicite:0]{index=0}

## Objectives
The main objective of this project is to reduce manual work in testing and improve software quality. It helps developers identify missing test cases and understand which tool gives better results for their code. It also provides a single platform where test generation, execution, and evaluation are done together.

## Features
- Upload Python source files for testing  
- Submit GitHub repository for analysis  
- Select specific modules for test generation  
- Generate unit tests using multiple tools  
- Execute generated tests automatically  
- Analyze coverage using line, branch, and mutation metrics  
- Compare results from different tools  
- View results in a simple dashboard  
- Export results into files  
- Maintain logs for execution and errors  

## System Workflow
The working of the system follows a clear flow. First, the user uploads Python files or provides a repository link. Then the user selects which files to test and chooses the tools for generating test cases. After configuration, the system generates unit tests and executes them. Once execution is complete, the system calculates coverage metrics and displays results in the dashboard. Finally, the user can compare results and export reports.

## System Architecture
The system is designed using a modular structure. It includes separate layers for user interaction, test generation, analysis, and system support. This design makes the system easy to understand and extend. All components work together to ensure smooth execution from input to result.

## Technologies Used
- Python  
- Streamlit for user interface  
- Pandas for data handling  
- Plotly for visualization  
- Open-source test generation tools  

## Installation
To run this project, first install all required packages using the following command:

pip install streamlit pandas numpy plotly

## How to Run
After installing the dependencies, run the application using:

streamlit run pytcg_eval.py

## Usage
Once the application starts, open it in the browser. Upload your Python files or provide a repository link. Select the files and configure test generation tools. Run the test generation process and wait for execution. After completion, view the results in the dashboard and export reports if needed.

## Coverage Metrics
The system provides three important metrics. Line coverage shows how many lines of code are executed. Branch coverage shows how many decision paths are tested. Mutation coverage checks how well tests can detect changes in the code. These metrics help users understand the quality of testing.

## Limitations
The system is designed to run on a local machine and uses only open-source tools. It is suitable for small to medium-sized Python projects. It does not require cloud services and avoids unsafe operations.

## Future Improvements
The system can be improved by adding more test generation tools, better visualizations, and database support for storing results. It can also be extended for larger projects and team collaboration.

## Conclusion
PyTCG-Eval provides a complete solution for automated test generation and evaluation. It reduces manual effort, improves testing quality, and helps developers make better decisions. The system is simple to use and can be helpful for both learning and real-world development.
