gnome-terminal -- bash -c "cd ~/mqtt_wake_vue3+flask;python ./backend/main.py;exec bash;"
gnome-terminal -- bash -c "cd ~/mqtt_wake_vue3+flask;npx http-server ./frontend/dist;exec bash;"