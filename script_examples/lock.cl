; BASE HOOK FILE
(defun run_in_room_enter [tools, char]
    (if (== (:id char) 1)
      (do (# tools :echo "Welcome Antonin !")         true)
      (do (# tools :echo "You're not allowed here !") false)))

{
  :run_in_room_enter nil
  :run_in_room_leave nil
  :run_in_exit run_in_exit
  :run_on_use nil
  :run_on_char nil
}
