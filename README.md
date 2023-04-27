# GProject
This is a starter template for gdsfactory based layouts. You can avoid installing gdsfactory locally by using github codespaces as follows:
Click on the arrow next to `code` on the green button on the top right of the landing page. Select codespaces and create a new codespace on branch `master`.
After the codespace has been set up you can click in the bottom left corner saying codespaces. Then select open in VS Code (If you haven't installed VS Code yet, this is the moment to do so).
You will have to confirm opening links in VS Code (potentially multiple times). At some point the project should open up in VS Code. When inspecting the panel ports you will notice some ports are forwarded from the development container (codespace) to your local machine. These are used to connect to KLayout on your local machine (install if you haven't already).

## The sharp bits
At the current stage two more configuration steps need to be taken, that can hopefully be eliminated in the future:
1. Install KLive in KLayout
2. Run `klive_receiver.py` on your local machine. Make sure to install its dependencies `paho-mqtt` and `requests` beforehand.

## The Cool Stuff
Now you can use gdsfactory to its full extent (including all features only available on linux). When you call `c.show()` on a component it should be rendered in KLayout if it is opened on your local machine. As an example you can run `python simple_layout.py` in the development container (which should be open in VS Code).

Have Fun!
