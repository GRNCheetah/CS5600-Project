

RADIO1 = '\t<input type="radio" name="{}" value="{}"{}> {} <br>\n'
RADIO2 = '\t<input type="radio" id="{}" name="{}" value="{}"{}>\n'
LABEL = '\t<label for="{}">{}</label>\n'
CHECKBOX = '\t<input type="checkbox" name="{}" value="{}"{}> {} <br>\n'

with open("questions.txt") as file:
    q_num = 1
    html = '''{% extends 'base.html' %}

{% block title %}Quiz{% endblock %}
{% block nav_quiz %}active{% endblock %}

{% block content %}

<form name="quiz" method="POST">
<h3><b>Part 1: </b> Which answer comes closer to telling how you usually feel or act?</h3>
<div class="quiz_wrapper">\n'''
    while q_num <= 25:
        question = file.readline().strip()
        q1 = file.readline().strip().split(" ")
        q2 = file.readline().strip().split(" ")

        html += "<div class='question'>" + question + ":</div>\n<div class='answer'>\n" + \
                RADIO1.format(q_num, q1[0], " required", " ".join(q1[1:])) + \
                RADIO1.format(q_num, q2[0], "", " ".join(q2[1:]))

        if q_num == 7:
            q3 = file.readline().strip().split(" ")
            html += RADIO1.format(q_num, q2[0], "", " ".join(q3[1:]))

        html += "</div>\n"

        file.readline()
        
        q_num += 1

    html += '</div>\n<h3><i>For this question, select all answers that are true.</i></h3>'

    question = file.readline().strip()
    q1 = file.readline().strip().split(" ")
    q2 = file.readline().strip().split(" ")
    q3 = file.readline().strip().split(" ")
    file.readline()

    html += question + "\n" + \
            CHECKBOX.format(q_num, q1[0], "", " ".join(q1[1:])) + \
            CHECKBOX.format(q_num, q2[0], "", " ".join(q2[1:])) + \
            CHECKBOX.format(q_num, q3[0], "", " ".join(q3[1:])) + "\n"
    
    q_num += 1

    html += '<h2><b>Part 2: </b> Which word in each pair appeals to you more?</h2>\n'

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

    html += '<button type="submit">Submit</button></form>\n{% endblock %}'
    

with open("quiz.html", "w") as file:
    file.write(html)

