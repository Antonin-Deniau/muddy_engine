-- BASE HOOK FILE
{
  run_in_room_enter = function(tools, room_id, char)
  end,

  run_in_room_leave = function(room, char)
  end,

  run_in_exit = function(tools, char)
    if char:id == 1 then
      tools:echo("Welcome Antonin !")
      return true
    else
      tools:echo("You're not allowed here !")
      return false
    end
  end,

  run_on_use = function(char, cmd)
  end,

  run_on_char = function(char, cmd)
  end,
}
