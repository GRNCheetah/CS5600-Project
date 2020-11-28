

RADIO1 = '\t<input type="radio" name="{}" value="{}"{}> {} <br>\n'
RADIO2 = '\t<input type="radio" id="{}" name="{}" value="{}"{}>\n'
LABEL = '\t<label for="{}">{}</label>\n'
CHECKBOX = '<label class="checkbox-container">{}\n\
\t<input type="checkbox" name="{}" value="{}">\n\
\t<span class="checkmark"></span>\n\
</label>\n'

with open("questions.txt") as file:
    q_num = 1
    html = '''<form name="quiz" method="POST">
<h2><b>Part 1: </b> Which answer comes closer to telling how you usually feel or act?</h2>'''
    while q_num <= 25:
        question = file.readline().strip()
        q1 = file.readline().strip().split(" ")
        q2 = file.readline().strip().split(" ")

        html += "<h3>" + question + "</h3>\n" + \
                RADIO1.format(q_num, q1[0], " required", " ".join(q1[1:])) + \
                RADIO1.format(q_num, q2[0], "", " ".join(q2[1:]))

        if q_num == 7:
            q3 = file.readline().strip().split(" ")
            html += RADIO1.format(q_num, q2[0], "", " ".join(q3[1:]))

        html += "\n"

        file.readline()
        
        q_num += 1

    html += '<h3><i>For this question, select all answers that are true.</i></h3>\n'

    question = file.readline().strip()
    q1 = file.readline().strip().split(" ")
    q2 = file.readline().strip().split(" ")
    q3 = file.readline().strip().split(" ")
    file.readline()

    html += "<h3>" + question + "</h3>\n" + \
            CHECKBOX.format(" ".join(q1[1:]), q_num, q1[0]) + \
            CHECKBOX.format(" ".join(q2[1:]), q_num, q2[0]) + \
            CHECKBOX.format(" ".join(q3[1:]), q_num, q3[0]) + "\n"
    
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

    html += '<button type="submit">Submit</button></form>'
    

with open("out.html", "w") as file:
    file.write(html)

