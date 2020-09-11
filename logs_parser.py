import subprocess

log_pods = subprocess.check_output(['kubectl', 'get', 'pods'])
pods_lines = log_pods.decode('UTF-8').split()

pod_template_name = 'dejan-tfjob-'
pod_names = []
for line in pods_lines:
    if line.startswith(pod_template_name) and 'worker' in line:
        pod_names.append(line.split('\s')[0])

for pod_name in pod_names:
    logs = subprocess.check_output(['kubectl', 'logs', pod_name])

    lines = logs.decode('UTF-8').split('\n')
    for line in lines: 
        if '1\timages/sec' in line:
            line_split = line.split('\s')
            start_time = line_split[0].split('|')[1]
        elif 'total images/sec' in line:
            line_split = line.split('\s')
            end_time = line_split[0].split('|')[1]
            
    spec_option = 'spec.nodeName=$(kubectl get pod ' + pod_name +  ' -o go-template="{{.spec.nodeName}}")'
            
    nvidia_line = subprocess.check_output(['kubectl', 'get', 'pod', '-A', '--field-selector', spec_option, 'grep', 'nvidia'])
    print(nvidia_line)

    print(pod_name, start_time, end_time)
