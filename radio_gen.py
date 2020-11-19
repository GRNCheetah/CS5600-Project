

RADIO = '<input type="radio" name="{}" value="{}"{}> {} <br>\n'
CHECKBOX = '<input type="checkbox" name="{}" value="{}"{}> {} <br>\n'

with open("questions.txt") as file:
    q_num = 1
    html = '''<form name="quiz" method="POST">
<h3><b>Part 1: </b> Which answer comes closer to telling how you usually feel or act?</h3>'''
    while q_num <= 25:
        question = file.readline().strip()
        q1 = file.readline().strip().split(" ")
        q2 = file.readline().strip().split(" ")

        html += "<h3>" + question + "</h3>\n" + \
                RADIO.format(q_num, q1[0], " required", " ".join(q1[1:])) + \
                RADIO.format(q_num, q2[0], "", " ".join(q2[1:]))

        if q_num == 7:
            q3 = file.readline().strip().split(" ")
            html += RADIO.format(q_num, q2[0], "", " ".join(q3[1:]))

        html += "\n"

        file.readline()
        
        q_num += 1

    html += '<h3><i>For this question, select all answers that are true.</i></h3>'

    question = file.readline().strip()
    q1 = file.readline().strip().split(" ")
    q2 = file.readline().strip().split(" ")
    q3 = file.readline().strip().split(" ")
    file.readline()

    html += "<h3>" + question + "</h3>\n" + \
            CHECKBOX.format(q_num, q1[0], " required", " ".join(q1[1:])) + \
            CHECKBOX.format(q_num, q2[0], "", " ".join(q2[1:])) + \
            CHECKBOX.format(q_num, q3[0], "", " ".join(q3[1:])) + "\n"
    
    q_num += 1

    html += '<h3><b>Part 2: </b> Which word in each pair appeals to you more?</h3>'

    while q_num <= 50:
        q1 = file.readline().strip().split()
        q2 = file.readline().strip().split()

        html += RADIO.format(q_num, q1[0], " required", " ".join(q1[1:])) + \
                RADIO.format(q_num, q2[0], "", " ".join(q2[1:]))

        html += "<br>\n"

        file.readline()
        
        q_num += 1

    html += '<button type="submit">Submit</button></form>'
    

with open("out.html", "w") as file:
    file.write(html)
