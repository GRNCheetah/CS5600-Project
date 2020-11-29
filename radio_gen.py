

RADIO1 = '\t<input type="radio" name="{}" value="{}"{}> {} <br>\n'
RADIO2 = '\t<input type="radio" id="{}" name="{}" value="{}"{}>\n'
LABEL = '\t<label for="{}">{}</label>\n'
PART1_RADIO = '''\t<label class="part-1-radio-container"> {} <br>
\t\t<input type="radio" name="{}" value="{}" {}>
\t\t<span class="radiobutt"></span>
\t</label>'''
CHECKBOX = '<label class="checkbox-container">{}\n\
\t<input type="checkbox" name="{}" value="{}">\n\
\t<span class="checkmark"></span>\n\
</label>\n'

with open("questions.txt") as file:
    q_num = 1
    html = '''{% extends 'base.html' %}

{% block title %}Quiz{% endblock %}
{% block nav_quiz %}active{% endblock %}

{% block content %}

<form name="quiz" method="POST">
<div class="quiz-part-1">
<h2><b>Part 1: </b> Which answer comes closer to telling how you usually feel or act?</h2>
<div class="quiz-part-1-grid">\n'''
    while q_num <= 25:
        question = file.readline().strip()
        q1 = file.readline().strip().split(" ")
        q2 = file.readline().strip().split(" ")

        html += "<div class='question'>" + question + ":</div>\n<div class='answer'>\n" + \
                PART1_RADIO.format(" ".join(q1[1:]), q_num, q1[0], " required") + \
                PART1_RADIO.format(" ".join(q2[1:]), q_num, q2[0], "")

        if q_num == 7:
            q3 = file.readline().strip().split(" ")
            html += PART1_RADIO.format(" ".join(q3[1:]), q_num, q3[0], "")

        html += "</div>\n"

        file.readline()
        
        q_num += 1

    html += '</div>\n<h3><i>For this question, select all answers that are true.</i></h3>\n<div class="quiz-part-1-grid">\n<div class="question">'

    question = file.readline().strip()
    q1 = file.readline().strip().split(" ")
    q2 = file.readline().strip().split(" ")
    q3 = file.readline().strip().split(" ")
    file.readline()

    html += question + "</div>\n<div class='answer'>\n" + \
            CHECKBOX.format(" ".join(q1[1:]), q_num, q1[0]) + \
            CHECKBOX.format(" ".join(q2[1:]), q_num, q2[0]) + \
            CHECKBOX.format(" ".join(q3[1:]), q_num, q3[0]) + "</div>\n"
    
    q_num += 1

    html += '</div>\n</div>\n<div class="quiz-part-2"><h2><b>Part 2: </b> Which word in each pair appeals to you more?</h2>\n<div class="quiz-part-2-grid">\n'

    while q_num <= 50:
        q1 = file.readline().strip().split()
        q2 = file.readline().strip().split()

        html += '<div class="radio-toolbar">\n'
        html += RADIO2.format(str(q_num)+"a", q_num, q1[0], " required") + \
                LABEL.format(str(q_num)+"a", " ".join(q1[1:])) + \
                RADIO2.format(str(q_num)+"b", q_num, q2[0], "") + \
                LABEL.format(str(q_num)+"b", " ".join(q2[1:]))
        html += '</div>\n'

        html += "<br>\n"

        file.readline()
        
        q_num += 1

    html += '</div>\n</div>\n<div class="center"><button class="submit-button" type="submit">Submit</button></div></form>\n{% endblock %}'
    

with open("quiz.html", "w") as file:
    file.write(html)

