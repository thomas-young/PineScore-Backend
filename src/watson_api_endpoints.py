import json
from ibm_watson import ToneAnalyzerV3

tone_analyzer = ToneAnalyzerV3(
    version='2019-05-27',
    iam_apikey='0w77Ioz4bZbFy0i9ydKC-5PYhTyIKRU9pulzn2wYcJKT',
    url='https://gateway.watsonplatform.net/tone-analyzer/api'
)

text = 'I really like the methods of evaluation because every person has their strengths, and I think that having a variety of ways to evaluate a student is really beneficial. It was nice to have tests, problem sets, data sets and a paper because it benefits everyone in the long run and it also helps us know if we know the material. Blah blah blah blah. I am so happy!!!'

text2 = 'There was an academic paper assigned for each class meeting with reading questions to answer and turn in before class. Each student had to present on a paper in class twice throughout the term. Then there was the final paper for the class, with several milestones throughout the term to encourage time management. The final paper was 15 pages max, not including tables/figures. Very reasonable amount of work. good mix. 2 midterms and a final. paper, problem sets, not that much work. 2 midterms, 2 data exercises (worked with an assigned partner), 6 problem sets, 1 final paper (no final exam). Workload is very fair 2 midterms, 6 problem sets, 2 data exercises, and one final paper (5-7 pages long). All very fair. Fair, plenty of time for assignments. I loved having 2 midterms and a final paper rather than a final test. I also found that the problem sets and data exercises taught me extremely beneficial skills for the future. I think overall methods of evaluation were fair. Overall a great mix, and not an overwhelming amount of work — two midterms, a final research paper, along with six problem sets and two data exercises. Problem sets, exams and final paper. Should give out longer tests with more questions (or do quizzes) rather than resting nearly everything on two 50-minute tests. The combination of exams and a paper was an excellent way to engage with the material and I felt the paper made me think of economics in a different, useful light. Thought the workload was super manageable and loved the balance between tests and papers. Two midterms, a paper, and problem sets. Weekly problem sets, 2 midterms, 2 partner short assignments and a final paper. good mix of assessments. light workload compared to other econ classes, lots of different evaluation methods. liked the mix of assignments. the exams were appropriate in testing the material, the data exercises were useful for the final paper'

text3 = 'this course is chill like a Hanover winter. i would recommend anyone interested in AI and cognitive computing to take it! i would DEFINITELY reccomend this class to my friends.'

tone_analysis = tone_analyzer.tone(
    {'text': text3},
    content_type='application/json',
).get_result()

print(json.dumps(tone_analysis, indent=2))
