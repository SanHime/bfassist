# bfassist
Bf42 game-server management tool


Full source for bfa. A tool that is supposed to help with the administration of bf42 game servers offering plenty of
different frameworks for adding features.

For the future of bfa the following release-strategy is intended. There should be 3 master servers representing the 3 
version-stages of bfa:
The development, experimental and stable stage.

Each server will gain the ability to redirect connecting clients to the correct stage depending on version information 
the client will send alongside requests. Version information is further constituted by a branch code which is a code 
consisting of a single letter and digit as well as the number of the last revision of the files in the SVN repository.

For now only the development and experimental stages will run. Configure the 'setup.py' accordingly to which version you
want to download. Keep in mind that everything is still in development as of now and there are no fully stable versions.


For now the development of bfa will continue to run via svn and only bigger releases will be pushed to GitHub, starting
with this one.
