from pan_cnc.views import *
from pan_cnc.lib.actions.DockerAction import DockerAction


class DockerTestView(CNCBaseFormView):
    snippet = 'docker_test'

    def form_valid(self, form):
        print('OK')
        workflow = self.get_workflow()
        docker_image = workflow.get('image')
        docker_cmd = workflow.get('cmd')

        docker_client = DockerAction()
        docker_client.docker_image = docker_image
        docker_client.docker_cmd = docker_cmd

        r = docker_client.execute_template(template='')

        context = dict()
        context['results'] = r
        return render(self.request, 'pan_cnc/results.html', context)


class IronSkilletWorkflow01(CNCBaseFormView):

    def generate_dynamic_form(self):
        self.fields_to_render = ['PANORAMA_TYPE', 'MGMT_TYPE']
        return super().generate_dynamic_form()

    def form_valid(self, form):
        panorama_type = self.get_value_from_workflow('PANORAMA_TYPE', '')
        mgmt_type = self.get_value_from_workflow('MGMT_TYPE', '')

        if panorama_type == 'static' or mgmt_type == 'static':
            print('we need some info from the user')
            self.next_url = 'workflow02'
        else:
            print('no info needed')
            self.next_url = 'workflow03'

        return super().form_valid(form)


class IronSkilletWorkflow02(CNCBaseFormView):

    def generate_dynamic_form(self):
        panorama_type = self.get_value_from_workflow('PANORAMA_TYPE', '')
        print(panorama_type)
        if panorama_type == 'static':
            print('adding panorama static fields')
            self.fields_to_render += ['PANORAMA_IP', 'PANORAMA_MASK']

        mgmt_type = self.get_value_from_workflow('MGMT_TYPE', '')
        print(mgmt_type)
        if mgmt_type == 'static':
            print('adding mgmt static fields')
            self.fields_to_render += ['MGMT_IP', 'MGMT_MASK']

        return super().generate_dynamic_form()
