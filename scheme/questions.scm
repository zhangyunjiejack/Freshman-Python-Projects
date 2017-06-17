(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cddr x) (cdr (cdr x)))
(define (cadar x) (car (cdr (car x))))

; Some utility functions that you may find useful to implement.
(define (map proc items)
    (cond
        ((null? items) nil)
        (else (cons (proc (car items)) (map proc (cdr items))))


    )
)

(define (cons-all first rests)
    (cond
        ((null? rests) nil)
        (else (cons (cons first (car rests)) (cons-all first (cdr rests)) )

    )

))

(define (zip pairs)
  (cond
      ((null? pairs) nil)
      (else (cons (map (lambda (expr) (car expr)) pairs) (cons (map (lambda (expr) (car (cdr expr))) pairs) nil)))
  )
)

;; Problem 18
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN Question 18
  (define (helper i s)
      (cond
          ((null? s) nil)
          (else (cons (cons i (cons (car s) nil))
                      (helper (+ i 1) (cdr s))))

      )
  )
  (helper 0 s)
  )
  ; END Question 18

;; Problem 19
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN Question 19
  (cond
      ((null? denoms) nil)
      ((> (car denoms) total) (list-change total (cdr denoms)))
      ((= 0 total) nil)
      ((= total (car denoms)) (cons (cons (car denoms) nil) (list-change total (cdr denoms))))
      (else  (append (cons-all (car denoms) (list-change (- total (car denoms)) denoms))
                    (list-change total (cdr denoms))))


  )

  )
  ; END Question 19

;; Problem 20
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (analyze expr)
  (cond ((atom? expr)
         ; BEGIN Question 20
         'REPLACE-THIS-LINE
         expr

         ; END Question 20
         )
        ((quoted? expr)
         ; BEGIN Question 20
         'REPLACE-THIS-LINE
         expr

         ; END Question 20
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
           'REPLACE-THIS-LINE
           (cond
           ((eq? 'define form) (cons 'lambda (cons (map analyze params) (cons (map analyze body) nil))))
           (else (cons form (cons (map analyze params) (map analyze body))))
           )
           ; END Question 20
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN Question 20
           'REPLACE-THIS-LINE
           (define expression (zip values))
           (cons (cons 'lambda (cons (car expression) (map analyze body))) (map analyze (cadr expression)))

           ; END Question 20
           ))
        (else
         ; BEGIN Question 20
         'REPLACE-THIS-LINE
         (cons (car expr) (map analyze (cdr expr)))


         ; END Question 20
         )))

;; Problem 21 (optional)
;; Draw the hax image using turtle graphics.
  (define (hax d k)
    ; BEGIN Question 21
      (define (repeat k fn)
          (if (> k 0)
                (begin (fn) (repeat (- k 1) fn))
                nil))

      (define (hexa fn)
          (repeat 6 (lambda () (fn) (lt 60))))

      (define (leg d k)
          (hax (/ d 2) (- k 1))
          (penup)
          (fd d)
          (pendown))

      (cond
          ((= k 0) (hexa (lambda () (fd d))))
          (else (repeat 3 (lambda () (begin
                                  (hax (/ d 2) (- k 1))
                                  (fd d)
                                  (lt 60)
                                  (fd d)
                                  (lt 60)

          ))))
      )
    )



  ; END Question 21
