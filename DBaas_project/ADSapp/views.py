import os
from django.http import JsonResponse
from rest_framework import viewsets
from django.conf import settings
from userAuth_app.models import User
import ldap
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from userAuth_app.permissions import IsAllowedRole
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from provider1_api.models import Provider
import ldap
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt
def kubectl_command(request):
    if request.method == 'POST':
        try:
            # Extracting the required fields from the POST data
            provider_name = request.data.get('provider')
            selected_key_name = request.data.get('selectedK8sKeyName')
            user_id = request.user.id  # Assuming you're using Django's built-in User model

            # Fetch the Provider instance matching the provider name, user ID, and selected key name
            provider = get_object_or_404(Provider, provider_name=provider_name, user_id=user_id, K8s_key_name=selected_key_name)
            
            # Retrieve the kubeconfig data from the Provider instance
            kubeconfig_data = provider.kubeconfig_data
            print('Kubeconfig Data:', kubeconfig_data)

            # Extract the command from the request data
            command = request.data.get('command')
            if not command:
                return HttpResponseBadRequest("No command provided")

            # Write kubeconfig data to a temporary file or use it directly depending on how kubectl is being invoked
            kubeconfig_path = "/path/to/kubeconfig/file"  # Define the path where you'll store kubeconfig data temporarily
            with open(kubeconfig_path, 'w') as f:
                f.write(kubeconfig_data)

            # Construct and execute the kubectl command using the kubeconfig
            command_list = ['kubectl', '--kubeconfig', kubeconfig_path] + command.split()

            result = subprocess.run(command_list, capture_output=True, text=True, check=True)
            return JsonResponse({'output': result.stdout, 'error': result.stderr})

        except subprocess.CalledProcessError as e:
            return JsonResponse({'output': e.stdout, 'error': e.stderr, 'returncode': e.returncode}, status=400)
    else:
        return HttpResponseNotAllowed(['POST'])

class FormViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAllowedRole]
    def create(self, request):
        print('api call')
        ldap_server_uri = request.data.get('ldapServerURI')
        ldap_server_bind_on = request.data.get('ldapServerBIND_DN')
        ldap_server_bind_password = request.data.get('ldapServerBIND_PASSWORD')
        ldap_group_search = request.data.get('ldapGroupSearch')
        is_connected = request.data.get('True')
        print('ldap_group_search', ldap_group_search)
        print('ldapServerBIND_PASSWORD :', ldap_server_bind_password)
        try:
            # Read the contents of the settings.py file
            with open(settings.BASE_DIR / 'DBaas_project' / 'settings.py', 'r') as settings_file:
                lines = settings_file.readlines()
            # Write the lines back to the settings.py file, updating only the AUTH_LDAP_SERVER_URI variable
            with open(settings.BASE_DIR / 'DBaas_project' / 'settings.py', 'w') as settings_file:
                for line in lines:
                    if line.startswith('AUTH_LDAP_SERVER_URI'):
                        settings_file.write(f"AUTH_LDAP_SERVER_URI = '{ldap_server_uri}'\n")
                    elif line.startswith('AUTH_LDAP_BIND_DN'):
                        settings_file.write(f"AUTH_LDAP_BIND_DN = '{ldap_server_bind_on}'\n")
                    elif line.startswith('AUTH_LDAP_BIND_PASSWORD'):
                        settings_file.write(f"AUTH_LDAP_BIND_PASSWORD = '{ldap_server_bind_password}'\n")
                    elif line.startswith('ldapGroupSearch'):
                        settings_file.write(f"ldapGroupSearch = '{ldap_group_search}  '\n")
                    elif line.startswith('IS_CONNNECTED'):
                        settings_file.write(f"IS_CONNNECTED = '{is_connected}  '\n")
                    else:
                        settings_file.write(line)
                     # AUTH_LDAP_GROUP_SEARCH = LDAPSearch("CN=Users,DC=os3,DC=com", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
            return JsonResponse({'message': 'LDAP settings updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    def reset_ldap_settings(request):
        try:
            # Update settings.py dynamically
            with open(os.path.join(settings.BASE_DIR, 'DBaas_project', 'settings.py'), 'a') as settings_file:
                settings_file.write("AUTH_LDAP_SERVER_URI = ''\n")
                settings_file.write("AUTH_LDAP_BIND_DN = ''\n")
                settings_file.write("AUTH_LDAP_BIND_PASSWORD = ''\n")
                settings_file.write("IS_CONNNECTED = ''\n")
            return JsonResponse({'message': 'LDAP settings disabled successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated,IsAllowedRole])
def get_ad_users(request):
    try:
        # Establish LDAP connection
        ldap_server_uri = 'ldap://10.0.0.2:389'
        bind_dn = 'CN=Administrator,CN=Users,DC=os3,DC=com'
        bind_password = 'P@33w0rd'
        ldap_connection = ldap.initialize(ldap_server_uri)
        ldap_connection.simple_bind_s(bind_dn, bind_password)
        search_base = 'CN=Users,DC=os3,DC=com'
        search_filter = "(sAMAccountName=*)"  # Filter to retrieve all users
        ldap_users = ldap_connection.search_s(
            search_base,
            ldap.SCOPE_SUBTREE,
            search_filter,
            ['sAMAccountName']
        )
        print("ldap_users:" ,ldap_users)
        # Extract usernames
        user_names = [entry.get('sAMAccountName', [])[0].decode('utf-8') for dn, entry in ldap_users]
        return JsonResponse({'user_names': user_names}, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
