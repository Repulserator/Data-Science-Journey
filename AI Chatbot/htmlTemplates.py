css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063;
    padding: 10px 0;
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn0.iconfinder.com/data/icons/geek-zone-icons-rounded/110/Eve-512.png">
    </div>  
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/f70280ae-f87e-4527-a0c4-abf90cdec2b4/dc70o6n-e05b0b1e-ba93-4f2d-9de7-e0065520f257.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcL2Y3MDI4MGFlLWY4N2UtNDUyNy1hMGM0LWFiZjkwY2RlYzJiNFwvZGM3MG82bi1lMDViMGIxZS1iYTkzLTRmMmQtOWRlNy1lMDA2NTUyMGYyNTcuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.9W-I31b_NNmpUPWKw4aKo8wzY9-zb_V_V6qMvrJGaAs">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
