from setuptools import find_packages, setup

setup(name='pptx-controller',
      version='0.1',
      license='MIT',
      description='Programs that can control PowerPoint over the network and mirror to client the presentation note.',
      author='BlaCkinkGJ',
      author_email='ss5kijun@gmail.com',
      url='https://github.com/blackinkgj/pptx-note-mirror-program',
      install_requires=[],
      packages=find_packages(),
      keywords=['pptx', 'win32com', 'remote'],
      python_requires='>=3',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'
      ],
      zip_safe=False
)
