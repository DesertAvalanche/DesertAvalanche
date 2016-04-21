def decay_points(memberships):
    for x in memberships :
        x.score = x.score*.9999

class VoteSystem():
    def can_vote(self,user,event):
        return True
    def handle_page(self,path,request,user,event):
        return "ERROR"
    def get_billboard(self,event):
        return "ERROR"
    def vote(self,member,event) :
        """return a vote"""
        return None
    def finalize(self,event) :
        """mutate the scores"""
        pass

