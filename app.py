from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are FlowerBot, a flower information chatbot.

You ONLY answer questions related to flowers.

You can explain:
- Flower names
- Types of flowers
- Flower colors
- Flower meanings
- Flower care
- Growing flowers
- Flower seasons
- Flower habitats
- Botanical information
- Interesting flower facts

If the user asks anything unrelated to flowers, politely say:
"🌸 Sorry! I can answer only flower-related questions."

Give clear, friendly and useful answers.
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>FlowerBot 🌸</title>
<style>
*{box-sizing:border-box}
body{
margin:0;
font-family:Arial,sans-serif;
background:linear-gradient(135deg,#ffdde1,#ee9ca7);
height:100vh;
display:flex;
align-items:center;
justify-content:center
}
.chat{
width:95%;
max-width:800px;
height:90vh;
background:white;
border-radius:25px;
box-shadow:0 20px 50px #0003;
display:flex;
flex-direction:column;
overflow:hidden
}
.header{
padding:25px;
background:linear-gradient(135deg,#ff4b91,#ff8fab);
color:white;
text-align:center
}
.header h1{margin:0}
.header p{margin:8px 0 0}
.messages{
flex:1;
padding:20px;
overflow-y:auto;
background:#fff8fb
}
.msg{
padding:13px 17px;
margin:10px 0;
border-radius:18px;
max-width:80%;
line-height:1.5;
white-space:pre-wrap
}
.user{
margin-left:auto;
background:#ff4b91;
color:white
}
.bot{
background:#ffe3ed;
color:#333
}
.input-area{
display:flex;
padding:15px;
gap:10px;
border-top:1px solid #ddd
}
input{
flex:1;
padding:15px;
border:1px solid #ddd;
border-radius:30px;
font-size:16px;
outline:none
}
button{
border:0;
border-radius:30px;
padding:0 25px;
background:#ff4b91;
color:white;
font-size:16px;
cursor:pointer
}
button:hover{background:#e6387c}
</style>
</head>
<body>
<div class="chat">
<div class="header">
<h1>🌸 FlowerBot</h1>
<p>Your Friendly Flower Information Assistant</p>
</div>

<div class="messages" id="messages">
<div class="msg bot">🌸 Hello! Ask me anything about flowers!</div>
</div>

<div class="input-area">
<input id="input" placeholder="Ask about a flower..." onkeydown="if(event.key==='Enter')send()">
<button onclick="send()">Send</button>
</div>
</div>

<script>
async function send(){
let input=document.getElementById("input");
let text=input.value.trim();
if(!text)return;

add(text,"user");
input.value="";

let response=await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:text})
});

let data=await response.json();
add(data.reply,"bot");
}

function add(text,type){
let box=document.getElementById("messages");
let div=document.createElement("div");
div.className="msg "+type;
div.textContent=text;
box.appendChild(div);
box.scrollTop=box.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message", "")

    try:
        prompt = SYSTEM_PROMPT + "\n\nUser Question:\n" + message

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )

        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": "⚠️ Something went wrong. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)