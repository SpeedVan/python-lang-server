import jupyter_client
import time
from jupyter_client.kernelspec import KernelSpecManager, NoSuchKernel, NATIVE_KERNEL_NAME
from IPython.utils.capture import capture_output
from ipython_genutils.tempdir import TemporaryDirectory

TIMEOUT = 30
td = TemporaryDirectory()


km, kc = jupyter_client.manager.start_new_kernel(kernel_name='python3')

KernelSpecManager().get_kernel_spec('python3')
with capture_output() as io:
    reply = kc.execute_interactive("print('hello')", timeout=TIMEOUT)
    print(reply)
    print(io.stdout)
# assert 'hello' in io.stdout
# assert reply['content']['status'] == 'ok'

kc.execute("print('hello world')")
kc.get_shell_msg() 

time.sleep(10)