import voting
from flask_wtf import Form
from wtforms import RadioField,StringField
from flask import render_template,redirect
class OptionForm(Form):
    choice = RadioField(choices=[])
    suggestion = StringField("suggestion")

class Democratic(voting.VoteSystem):
    def __init__(self,event,model) :
        self.event = event
        self.model = model
    def handle_page(self,path,request,member) :
        form = OptionForm(obj=self.get_scores().keys())
        if request.method == "POST" :
            if form.validate_on_submit() :
                print(form.suggestion.data)
                print(form.choice.data)
                if form.suggestion.data != "" :
                    pass
                elif form.choice.data != "" :
                    pass
        return render_template("democratic/vote.html",event=self.event,form=form)
        pass
    def get_billboard(self,member) :
        return render_template("democratic/billboard.html",event=self.event)
    def get_scores(self) :
        out = {}
        for x in self.event.votes :
            if x.data not  in out :
                out[x.data] = 0
            out[x.data] += 1
        return out

def factory(event,model):
    return Democratic(event,model)
