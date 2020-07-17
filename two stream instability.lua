-- Gkyl ------------------------------------------------------------------------
local Plasma = require("App.PlasmaOnCartGrid").VlasovMaxwell

knumber = 0.5 -- wave-number
elVTerm = 0.2 -- electron thermal velocity
vDrift = 1.0 -- drift velocity
perturbation = 1.0e-6 -- distribution function perturbation

app = Plasma.App {
   logToFile = false,

   tEnd = 200.0, -- end time
   nFrame = 200, -- number of output frames
   lower = {-math.pi/knumber}, -- configuration space lower left
   upper = {math.pi/knumber}, -- configuration space upper right
   cells = {16}, -- configuration space cells
   basis = "serendipity", -- one of "serendipity" or "maximal-order"
   polyOrder = 2, -- polynomial order
   timeStepper = "rk3", -- one of "rk2", "rk3" or "rk3s4"
   cflFrac = 0.9,
   -- decomposition for configuration space
   decompCuts = {1}, -- cuts in each configuration direction
   useShared = true, -- if to use shared memory

   -- boundary conditions for configuration space
   periodicDirs = {1}, -- periodic directions
   bcx = { }, -- boundary conditions in X

   -- electrons
   elc = Plasma.Species {
      --nDistFuncFrame = 2,
      
      charge = -1.0, mass = 1.0,
      -- velocity space grid
      lower = {-6.0},
      upper = {6.0},
      cells = {16},
      decompCuts = {1},
      -- initial conditions
      init = function (t, xn)
	 local x, v = xn[1], xn[2]
	 local alpha = perturbation
	 local k = knumber
	 local vt = elVTerm
	 
	 local fv = 0.5/math.sqrt(2*math.pi*vt^2)*(math.exp(-(v-vDrift )^2/(2*vt^2))+math.exp(-(v+vDrift)^2/(2*vt^2)))
	 return (1+alpha*math.cos(k*x))*fv
      end,
      evolve = true, -- evolve species?

      diagnosticMoments = { "M0", "M1i", "M2" }
   },

   -- field solver
   field = Plasma.Field {
      epsilon0 = 1.0, mu0 = 1.0,
      init = function (t, xn)
	 local alpha = perturbation
	 local k = knumber
	 return -alpha*math.sin(k*xn[1])/k, 0.0, 0.0, 0.0, 0.0, 0.0
      end,
      evolve = true, -- evolve field?
   },
}
-- run application
app:run()
