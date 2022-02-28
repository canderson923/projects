


(define (problem mixed-f2-p1-u0-v0-g0-a0-n0-A0-B0-N0-F0-r0)
   (:domain miconic)
   (:objects p0 p1 p2 p3 p4 - passenger
             e0 e1 e2 - elevator
             f0 f1 f2 f3 f4 f5 f6 f7 - floor)


(:init
;;floors
(above f0 f1)
(above f0 f2)
(above f0 f3)
(above f0 f4)
(above f0 f5)
(above f0 f6)
(above f0 f7)

(above f1 f2)
(above f1 f3)
(above f1 f4)
(above f1 f5)
(above f1 f6)
(above f1 f7)

(above f2 f3)
(above f2 f4)
(above f2 f5)
(above f2 f6)
(above f2 f7)

(above f3 f4)
(above f3 f5)
(above f3 f6)
(above f3 f7)

(above f4 f5)
(above f4 f6)
(above f4 f7)

(above f5 f6)
(above f5 f7)

(above f6 f7)

;;People

(origin p0 f7)
(destin p0 f6)

(origin p1 f6)
(destin p1 f0)

(origin p2 f5)
(destin p2 f0)

(origin p3 f4)
(destin p3 f0)

(origin p4 f3) 
(destin p4 f0)

;;elevators
(lift-at e0 f0)
(lift-at e1 f0)
(lift-at e2 f0)

)


(:goal (forall (?p - passenger) (served ?p)))

)

