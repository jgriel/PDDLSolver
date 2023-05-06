(define (domain pass-the-ball)
   (:predicates (has-first-letter ?n ?l)
		(has-last-letter ?n ?l)
		(in-room ?n ?r)
		(has-ball ?n)
        (is-room ?r))

   (:action pass
       :parameters  (?from ?to ?letter ?room)
       :precondition (and  (in-room ?from ?room) (in-room ?to ?room) (has-ball ?from) (has-first-letter ?to ?letter) (has-last-letter ?from ?letter))
       :effect (and  (has-ball ?to)
		     (not (has-ball ?from))))
		     
    (:action move
        :parameters (?person ?from ?to)
        :precondition (and (in-room ?person ?from) (is-room ?from) (is-room ?to))
        :effect (and (in-room ?person ?to) (not (in-room ?person ?from))))
    )