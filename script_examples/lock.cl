; BASE HOOK FILE

(defasync run_on_exit [tools, char]
    (if (== (:id char) 1)
      (do (await (# tools :echo "Welcome Antonin !"))         true)
      (do (await (# tools :echo "You're not allowed here !")) false)))

{
  :run_on_room_enter nil
  :run_on_room_leave nil
  :run_on_exit run_on_exit
  :run_on_use nil
  :run_on_char nil
}
