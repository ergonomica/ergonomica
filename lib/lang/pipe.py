class Pipeline:
    def __init__(self):
        pass
    
class StaticPipeline(Pipeline):
    def __init__(self):
        self.args = [None, None]
        self.kwargs = [None, None]
    def getstack_args(self,index=-1):
        try:
            return self.args[index]
        except IndexError:
            return None

    def getstack_kwargs(self,index=-1):
        try:
            return self.kwargs[index]
        except IndexError:
            return None
        
    def setstack_args(self,item):
        self.args.append(item)
        
    def setstack_kwargs(self, item):
        self.kwargs.append(item)

#class DynamicPipeline(Pipeline):
