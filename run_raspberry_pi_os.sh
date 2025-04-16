lxterminal -e "bash -c 'cd ~/mqtt_wake_vue3+flask;python ./backend/main.py; exec bash'"
lxterminal -e "bash -c 'cd ~/mqtt_wake_vue3+flask;npx http-server ./frontend/dist; exec bash'"