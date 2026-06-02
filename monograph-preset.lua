--[[
    MONOGRAPH STYLE PRESET for DaVinci Resolve Fusion
    Free Version Compatible
    
    INSTRUCTIONS:
    1. Copy this file to: ~/.local/share/DaVinciResolve/Fusion/Templates/
    2. In DaVinci Resolve, go to Fusion page
    3. Look for "Templates" or "Presets" in the Inspector
    4. Find "Monograph Cinematic" and apply to your clips
    
    OR:
    1. Open Fusion page
    2. Create a new Macro from the effects settings
    3. Paste this code to create an automated preset
]]

-- Monograph Cinematic Look Fusion Macro
{
    Notes = "Cinematic Monograph Style - Letterbox + Color Grade",
    Category = "Monograph",
    SubCategory = "Style Presets",
    Title = "Monograph Cinematic",
    
    -- Inputs for customization
    Inputs = {
        -- Crop Settings
        CropTop = { Link = "_crop.Top", Value = 0.13, Min = 0, Max = 0.5 },
        CropBottom = { Link = "_crop.Bottom", Value = 0.13, Min = 0, Max = 0.5 },
        
        -- Color Settings
        Saturation = { Link = "_primaries.Saturation", Value = 0.65, Min = 0, Max = 1.5 },
        LiftR = { Value = 0.010 },
        LiftG = { Value = 0.012 },
        LiftB = { Value = 0.020 },
        GammaR = { Value = 0.950 },
        GammaG = { Value = 0.950 },
        GammaB = { Value = 0.980 },
        GainR = { Value = 0.900 },
        GainG = { Value = 0.900 },
        GainB = { Value = 0.900 },
        
        -- Grain Settings
        GrainAmount = { Value = 0.08, Min = 0, Max = 0.5 },
    },
    
    -- Node Tree
    NodeGraph = [[
        +------------------------------------------------------+
        |                                                       |
        |   MediaIn ---+                                      |
        |              |                                      |
        |              +---> Primaries ---> Crop ---> Merge   |
        |                         |               ^            |
        |                         |               |            |
        |                         +---> Grain ----+            |
        |                         |                            |
        |              +-----------+                            |
        |              |                                        |
        |              +---> Background (Black) --> Crop -----> MediaOut
        |                                                       |
        +------------------------------------------------------+
    ]],
}

--[[
ALTERNATIVE: Simple Color Grade Only (without letterbox)
Paste this directly in Color Page Node Editor:

Node 1 (Primaries):
Saturation = 0.65
Contrast = 1.05
Pivot = 0.50
Lift R = 0.010, G = 0.012, B = 0.020
Gamma R = 0.950, G = 0.950, B = 0.980
Gain R = 0.900, G = 0.900, B = 0.900

Node 2 (Grain - if available in Free version):
Grain = 0.08, Size = 1.0, Color = Monochrome
]]

--[[
LETTERBOX CROP SETTINGS for Fusion Page:

1. Go to Fusion Page
2. Add MediaIn node
3. Add Crop node: MediaIn >> Crop >> MediaOut
4. In Crop settings:
   - Top: 0.13
   - Bottom: 0.13
   - Left: 0
   - Right: 0

For black bars background:
1. Add Background node (Solid Color > Black)
2. Add another Crop node
3. Merge both: Crop(Video) + Crop(Background) >> Merge >> MediaOut
]]

--[[
TEXT ANIMATION KEYFRAMES (Fusion Page):

Text+ Settings:
- Title: "NARUTO" (change to your subject)
- Font: Inter, SF Pro, or Roboto
- Size: 48
- Position: 0.5 (center X), 0.8 (80% Y)
- Color: 1,1,1 (white), Alpha: 0.8

Keyframe Setup (0:00 to 0:02):
At 0:00:00 - Scale: 0, Opacity: 0
At 0:02:00 - Scale: 1, Opacity: 1

Apply smooth interpolation (ease-in-out)
]]

--[[
SPEED RAMP SCRIPT (Edit Page):

To create speed ramps, use these settings:

1. Select clip on timeline
2. Right-click >> Change Clip Speed
3. For standard slow-mo: 50%
4. For dramatic: 25%
5. For speed ramp:
   - Uncheck "Maintain Pitch" for audio sync
   - Check "Speed Curve" 
   - Choose curve type: "Ease-In" or custom Bezier

Sample Speed Ramp Points:
Time 0:00 - Speed: 100%
Time 0:15 - Speed: 50% (ease-in over 3 seconds)
]]

--[[
MACRO: Monograph Full Edit Template
Copy this section into a .setting file in your Fusion Templates folder

This creates a complete letterboxed, color-graded clip with grain
]]

return {
    -- Preset Name
    Name = "Monograph Cinematic",
    
    -- Preset Data
    DataFlow = "template",
    
    -- Version
    Version = "1.0",
    
    -- The actual node structure
    Nodes = {
        -- Background (Black) for letterbox
        Background = {
            Active = true,
            Xpos = 0,
            Ypos = 0,
            Inputs = {
                Width = 1920,
                Height = 1080,
                ["Black"] = 1,
            }
        },
        
        -- Crop for background (creates top bar)
        CropBG_Top = {
            Active = true,
            Xpos = 0,
            Ypos = 1,
            Parent = 0, -- Background
            Inputs = {
                Top = 0.13,
                Bottom = 0,
                Left = 0,
                Right = 0,
            }
        },
        
        -- Crop for background (creates bottom bar)
        CropBG_Bottom = {
            Active = true,
            Xpos = 0,
            Ypos = 1,
            Parent = 0,
            Inputs = {
                Top = 0,
                Bottom = 0.13,
                Left = 0,
                Right = 0,
            }
        },
        
        -- Primary Color Correction
        Primaries = {
            Active = true,
            Xpos = 0,
            Ypos = 0,
            Inputs = {
                Saturation = 0.65,
                Contrast = 1.05,
                -- Lift (Shadows)
                LiftR = 0.010,
                LiftG = 0.012,
                LiftB = 0.020,
                -- Gamma
                GammaR = 0.950,
                GammaG = 0.950,
                GammaB = 0.980,
                -- Gain
                GainR = 0.900,
                GainG = 0.900,
                GainB = 0.900,
            }
        },
        
        -- Crop for video (letterbox)
        CropVideo = {
            Active = true,
            Xpos = 0,
            Ypos = 1,
            Inputs = {
                Top = 0.13,
                Bottom = 0.13,
                Left = 0,
                Right = 0,
            }
        },
        
        -- Merge all elements
        Merge = {
            Active = true,
            Xpos = 0,
            Ypos = 2,
            Inputs = {
                -- Background crops merged first
                -- Then video crop on top
            }
        }
    },
    
    -- Connections
    Links = {
        { From = "Background", To = "CropBG_Top" },
        { From = "Background", To = "CropBG_Bottom" },
        { From = "Primaries", To = "CropVideo" },
        { From = "CropBG_Top", To = "Merge", Input = 0 },
        { From = "CropBG_Bottom", To = "Merge", Input = 0 },
        { From = "CropVideo", To = "Merge", Input = 1 },
    }
}