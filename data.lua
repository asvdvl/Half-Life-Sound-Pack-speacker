-- https://lua-api.factorio.com/latest/prototypes/ProgrammableSpeakerPrototype.html#instruments

-- https://lua-api.factorio.com/latest/types/ProgrammableSpeakerNote.html

local files_table = require("soundpack/files")
local cat_name_base = "hl-soundpack-"

local instruments = data.raw["programmable-speaker"]["programmable-speaker"].instruments
for cat_name, cat_sounds in pairs(files_table) do
    local instrument_name = cat_name_base..cat_name
    local instrument = {
        name = instrument_name,
        notes = {}
    }
    for _, sound_name in pairs(cat_sounds) do
        table.insert(instrument.notes, {name = instrument_name.."/"..sound_name, sound = {filename = "__base__/sound/eat-1.ogg"}})
    end
    table.insert(instruments, instrument)
end

