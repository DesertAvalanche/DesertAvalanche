import voting
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import render_template,redirect

class ChoiceForm(Form):
    choice = StringField("choice",validators=[DataRequired()])

class RoundRobin(voting.VoteSystem):
    def __init__(self,event,model):
        self.event= event
        self.model = model
    def can_vote(self,member):
        return member == self._get_voter()
    def handle_page(self,path,request,member):
        if self.can_vote(member) :
            form = ChoiceForm(request.form)
            if request.method == "POST" :
                if form.validate_on_submit():
                    if len(self.event.votes) > 0 :
                        self.event.votes[0].data = form.choice.data
                    else :
                        self._distribute_points(member)
                        self.model.Vote(member,self.event,form.choice.data)
                    self.model.db.session.commit()
                    return redirect(self.event.get_url())
            return render_template("roundrobin/vote.html",form=form,event=self.event)
        return "ERROR [{}]".format(path)
    def get_billboard(self, member) :
        return render_template("roundrobin/billboard.html",event=self.event,method=self,membership=member)
    def get_choice(self) :
        if len(self.event.votes) > 0 :
            return self.event.votes[0].data
        else :
            return None
    def _distribute_points(self,member) :
        voting.decay_points(self.event.group.memberships)
        member.score -= 1;
        for x in self.event.group.memberships :
            x.score += 1.0 / len(self.event.group.memberships)
    def _get_voter(self) :
        if len(self.event.votes) > 0 :
            return self.event.votes[0].membership
        return max(self.event.group.memberships,key=lambda x:x.score)

def factory(event,model):
    return RoundRobin(event,model)
