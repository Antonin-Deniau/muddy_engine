MUDDY ENGINE
============


Muddy engine is a MUD/MUCK like game engine,

### Features:
- [x] Multi account and registration
- [x] Multiplayer support
- [x] Scripting language support
- [x] Room and object creation
- [ ] Combat system
- [ ] Economic system
- [ ] Adminitstration system
- [ ] Web UI


### Script example:

A Muddy script is an implementation of the lisp/clojure language.
It define hooks to be run on certain MUD events.

```clojure
; BASE HOOK FILE

(defun run_on_exit [tools char]
    (if (= (:id char) 1)
      (do (# tools :echo (str "Welcome " (:name char) " !")) true)
      (do (# tools :echo "You're not allowed here !")        false)))

{
  :run_on_room_enter nil
  :run_on_room_leave nil
  :run_on_exit run_on_exit
  :run_on_use nil
  :run_on_char nil
}
```


### Implemented commands:

## Auth commands:
 - `register`: Register an account to the mud
 - `login`:    Login to an existing account
 - `create`:   Create a character
 - `choose`:   Choose a character to play as

## Character commands:
 - `move`:      Move your character to another room
 - `inventory`: List objects in your inventory
 - `look`:      Look around the room
 - `say`:       Say something in the room

## Builder commands:
 - `list`:           List object/room/exit/script you've created
 - `create`:         Create object/room/exit/script
 - `set`:            Set a property of an object/room/exit/script
 - `attach_script`:  Attach a script to something


## Client side command:
 - `upload`: Upload a file to an existing script
