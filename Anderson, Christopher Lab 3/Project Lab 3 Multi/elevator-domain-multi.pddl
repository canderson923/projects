;;Alt + P
(define (domain miconic)
  (:requirements :adl :typing)
  (:types passenger - object
          floor - object
          elevator - object
         )

(:predicates 
(origin ?person - passenger ?floor - floor)
;; entry of ?person is ?floor
;; inertia

(destin ?person - passenger ?floor - floor)
;; exit of ?person is ?floor
;; inertia

(above ?floor1 - floor  ?floor2 - floor)
;; ?floor2 is located above of ?floor1

(boarded ?elevator - elevator ?person - passenger)
;; true if ?person has boarded the lift

(served ?person - passenger)
;; true if ?person has alighted as her destination

(lift-at ?elevator - elevator ?floor - floor)
;; current position of the lift is at ?floor
)


;;stop

(:action stop
  :parameters (?e - elevator ?f - floor)
  :precondition (lift-at ?e ?f)
  :effect (and 
               (forall (?p - passenger) 
                  (when (and (boarded ?e ?p) 
                             (destin ?p ?f))
                        (and (not (boarded ?e ?p)) 
                             (served  ?p))))
               (forall (?p - passenger)                
                   (when (and (origin ?p ?f) (not (served ?p)))
                              (boarded ?e ?p)))))


;;drive up

(:action up
  :parameters (?e - elevator ?f1 - floor ?f2 - floor)
  :precondition (and (lift-at ?e ?f1) (above ?f1 ?f2))
  :effect (and (lift-at ?e ?f2) (not (lift-at ?e ?f1))))


;;drive down

(:action down
  :parameters (?e - elevator ?f1 - floor ?f2 - floor)
  :precondition (and (lift-at ?e ?f1) (above ?f2 ?f1))
  :effect (and (lift-at ?e ?f2) (not (lift-at ?e ?f1))))
)



