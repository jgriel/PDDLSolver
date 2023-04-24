(define (domain pass-the-ball)
    (:predicates (has-first-letter ?n ?l)
		(has-last-letter ?n ?l)
		(in-room ?n ?r)
		(has-ball ?n))   
        
   (:action laugh
       :parameters  (?from ?to ?letter ?room)
       :precondition (and  (in-room ?from ?room) (in-room ?to ?room) (has-ball ?from) (has-first-letter ?to ?letter) (has-last-letter ?from ?letter))
       :effect (and  (not (has-ball ?to))
		     (not (has-ball ?from))))

   (:action run
       :parameters  (?from ?to ?letter ?room)
       :precondition (and (not (in-room ?from ?room)) (in-room ?to ?room) (has-ball ?from) (has-first-letter ?to ?letter) (has-last-letter ?from ?letter))
       :effect (and  (has-ball ?to)
		     (not (has-ball ?from)) (in-room ?from ?room)))

   (:action pass
       :parameters  (?from ?to ?letter ?room)
       :precondition (and  (in-room ?from ?room) (in-room ?to ?room) (has-ball ?from) (has-first-letter ?to ?letter) (has-last-letter ?from ?letter))
       :effect (and  (has-ball ?to)
		     (not (has-ball ?from))))
	 
    
    (:action move
        :parameters (?from ?to ?person)
        :precondition (and (in-room ?person ?from))
        :effect (and (in-room ?person ?to) (not (in-room ?person ?from)) (has-ball ?to)))
		 
      
    )

