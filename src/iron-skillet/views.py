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

