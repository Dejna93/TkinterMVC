from Tkinter import *
from abc import ABCMeta,abstractmethod


class Controller(object):

    def __init__(self):
        self.models = {}
        self.views = {}

    def update(self):
        raise NotImplementedError()

    def destroy_frame(self):
        raise NotImplementedError()

    def add_model(self, model):
        self.models[model.get_key()] = model

    def add_view(self, view):
        self.views[view.get_key()] = view

    def get_model(self, key):
        return self.models[key]

    def get_view(self, key):
        return self.views[key]

    def get_models(self):
        return self.models

    def get_views(self):
        return  self.views

class View(Frame):

    def __init__(self, controller , name):
        self.controller = controller
        self.name = name
        self.frame = Frame()
        self.frame.grid(row=0 , column=0)

    def get_key(self):
        return self.name

    def show_frame(self):
        self.frame.tkraise()
        self.frame.update()
        self.frame.event_generate("<<ShowFrame>>")

class Model(object):

    def __init__(self, name):
        self.name = name

    def get_key(self):
        return self.name


class StlController(Controller):

    def __init__(self, parent):
        Controller.__init__(self)
        self.parent = parent
        self.add_model( STLModel(self, "stl"))
        self.add_view( STLView(self, "stl_view"))
        self.get_model("stl").add_to_stl("c://asds/sdsd")
        print self.get_model("stl").get_stls()

    def listChangedCallback(self):
        print "list change"

    def btn_click(self):
        self.parent.run_controller(TxtController)

class TxtController(Controller):

    def __init__(self, parent):
        Controller.__init__(self)
        self.parent = parent
        self.add_view(TxtView(self,"txt_view"))
        print  "Txt controller"

    def btn_click(self):
        self.parent.run_controller(StlController)

class TxtView(View):
    def __init__(self, controller,name):
        View.__init__(self,controller, name)
        self.button = Button(self.frame, text="TXT", command=self.controller.btn_click).grid(row=1, column = 1)



class STLModel(Model):

    def __init__(self, controller ,name):
        Model.__init__(self,name)
        self.controller = controller
        self.stl_list = []
        self.current_stl = ""

    def listChanged(self):
        self.controller.listChangedCallback()

    #Add unique path to the list
    def add_to_stl(self, path_stl ):
        if not path_stl in self.stl_list:
            self.stl_list.append(path_stl)
            self.listChanged()

    def get_stls(self):
        return self.stl_list

    def del_stl(self, path_stl):
        if path_stl == self.current_stl:
            self.current_stl = ""
        for path in self.stl_list:
            if path_stl == path:
                self.stl_list.remove(path)
                self.listChanged()



class STLView(View):

    def __init__(self, controller,name):
        View.__init__(self,controller, name)
        self.button = Button(self.frame, text="STL", command = self.controller.btn_click).grid(row=1, column = 1)




class MainController():

    def __init__(self, parent):
        self.parent = parent
        self.controllers = (StlController , TxtController)
        self.run_controller()

    def run_controller(self, controller=StlController):
        print "run controller"
        self.current_cont = self.controllers[self.controllers.index(controller)](self)




def main():
    root = Tk()
    root.minsize(800,600)
    frame = Frame(root)
    root.title("test mcv")
    app = MainController(root)
    root.mainloop()

if __name__ == '__main__':
    main()