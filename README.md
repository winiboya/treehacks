## Inspiration
ClassMate was inspired by the boom of OpenAI and ChatGPT. We sought a way to integrate the powerful tool of ChatGPT into classrooms to help students further explore academic concepts while also mitigating cheating and abuse of the AI tool.

## What it does
ClassMate compiles together a student's classes and topics covered in each class. Upon clicking each topic page, students are given concept-related prompts written by their teachers to help guide their exploration. Moreover, they are also given fill-in-the-blank sentence frames which they can fill out with specific topics/skills they would like to improve. These pre-generated prompts aim to guide students utilizing AI instead of allowing free roaming in order to discourage cheating. Prompts selected by the student are then inputted via the OpenAI API and an answer is returned to the student.

## How we built it
We started by building the core functionalities of our website through HTML, CSS, and Flask. We also used SQLite to build a database to store key website information like user logins and user class topics/questions. Once we had the website up, we embedded the OpenAI API to the class topics section to help with student questions. 

## Challenges we ran into
Building a database from scratch using SQLite was definitely not easy and took a lot of trial and error to get going. Also, it was challenging to code the HTML and CSS formatting, as well as getting correct inputs and outputs for various functions like user logins and user questions for the OpenAI API.

## Accomplishments that we're proud of
We're proud of being able to integrate the OpenAI API into our aesthetically pleasing and user-friendly website. We were also proud that we were able to turn a tool that is associated with possible academic abuse into a tool for improved student learning and teaching.



## Video
https://user-images.githubusercontent.com/90153773/219964125-6e9f1c5f-0fa8-49bd-ae1c-4e49394936ea.mov

