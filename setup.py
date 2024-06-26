from setuptools import find_packages,setup
from typing import List

def get_requirements(file_path:str)->List[str]:
    Hypen_e_dot="-e ."
    requiremnets =[]
    with open(file_path) as file_obj:
        requiremnets=file_obj.readlines()
        requiremnets = [ req.replace( '/n',"") for req in requiremnets]
        if Hypen_e_dot in requiremnets:
            requiremnets.remove(Hypen_e_dot)
    
    return requiremnets


    
setup(
    name="Ml Projects",
    version='0.0.1',
    author="Riswan Ahamed",
    author_email='riswanahamed38@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)