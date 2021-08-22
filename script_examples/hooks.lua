function run_in_room_enter(room, char)
end

function run_in_room_leave(room, char)
end

function run_in_exit(char, origin, dest)
end

function run_on_use(char, cmd)
end

function run_on_char(char, cmd)
end


return {
  run_in_room_enter = run_in_room_enter,
  run_in_room_leave = run_in_room_leave,
  run_in_exit = run_in_exit,
  run_on_use = run_on_use,
  run_on_char = run_on_char,
}
