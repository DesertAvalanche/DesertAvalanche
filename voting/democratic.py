import voting
from flask_wtf import Form
from wtforms import RadioField,StringField
from wtforms.validators import DataRequired
from flask import render_template,redirect
class OptionForm(Form):
    choice = RadioField("choices",choices=[])

class SuggestionForm(Form):
    suggestion = StringField("suggestion",validators=[DataRequired()])

class Democratic(voting.VoteSystem):
    def __init__(self,event,model) :
        self.event = event
        self.model = model
    def handle_page(self,path,request,member) :
        suggestionform = SuggestionForm()
        optionform = OptionForm()
        if path!="add" :
            scores = self.get_scores()
            print(scores)
            optionform.choice.choices=list(map(lambda x:(x[0],x[0]),self.sorted_scores()))
            if request.method == "POST" :
                if optionform.validate_on_submit() :
                    self.set_vote(member,optionform.choice.data)
                return redirect(self.event.get_url())
        else :
            if suggestionform.validate_on_submit() :
                self.set_vote(member,suggestionform.suggestion.data)
                return redirect(self.event.get_url())
            print("DID NOT VALIDATE")
        return render_template("democratic/vote.html",event=self.event,optionform=optionform,suggestionform=suggestionform,scores=scores)

    def get_billboard(self,member) :
        return render_template("democratic/billboard.html",event=self.event,scores=self.sorted_scores())
    def sorted_scores(self) :
        scores = self.get_scores()
        return list(map(lambda x:(x,scores[x]),sorted(scores.keys(),key=lambda x:scores[x])))
    def get_scores(self) :
        out = {}
        for x in self.event.votes :
            if x.data not  in out :
                out[x.data] = 0
            out[x.data] += 1
        return out

    def set_vote(self,member,data) :
        for x in self.event.votes :
            if x.membership == member :
                x.data = data
                self.model.db.session.commit()
                return
        self.model.Vote(member,self.event,data)
        self.model.db.session.commit()

def factory(event,model):
    return Democratic(event,model)
