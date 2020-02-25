subroutine lagint(y, dy, x, x2, x3, xo, m, n, l)
    integer m, n, l, i, j, k
    real*8 x2(m, n), x3(m, n), xo(l), y(l), dy(l)
    real*8 xi(m * n), yi(m * n)
    integer x, n0, nl, nr
    real*8 xin(x), yin(x), xi1, xi2, fi1, fi2

    !f2py intent(in) x, x2, x3, xo
    !f2py intent(out) y(l), dy(l)

    ! x - number of points = order + 1
    ! order of the interpolant must be <= max(m,n)
    if(x>max(m, n)) then
        x = max(m, n)
    endif

    do k = 1, l

        do i = 1, m * n
            if(m.eq.1) then
                xi(i) = x2(1, i)
                yi(i) = x3(1, i)
            else
                xi(i) = x2(i, 1)
                yi(i) = x3(i, 1)
            endif
        enddo
        !

        ! nearest nod in the grid right to xo
        do i = 1, m * n
            if(xo(k).le.xi(i)) then
                n0 = i;
                exit
            endif
        enddo
        ! number of elements left to xo
        nl = n0 - 1
        ! number of elements right to xo
        nr = m * n - n0 + 1
        !      nr = m*n - n0
        ! cut x points around xo
        if(floor(dble(x) / 2)>nl) then
            xin = xi(1:x)
            yin = yi(1:x)
        endif
        if(ceiling(dble(x) / 2)>nr) then
            xin = xi(m * n - x + 1:m * n)
            yin = yi(m * n - x + 1:m * n)
        endif
        if((floor(dble(x) / 2)<=nl).and.(ceiling(dble(x) / 2)<=nr)) then
            xin = xi(n0 - floor(dble(x) / 2):n0 + ceiling(dble(x) / 2) - 1)
            yin = yi(n0 - floor(dble(x) / 2):n0 + ceiling(dble(x) / 2) - 1)
        endif

        ! Subroutine performing the Lagrange interpolation with the
        ! Aitken method. y: interpolated value. dy: error estimated.

        do  i = 1, x
            do  j = 1, x - i
                xi1 = xin(j)
                xi2 = xin(j + i)
                fi1 = yin(j)
                fi2 = yin(j + 1)
                yin(j) = (xo(k) - xi1) / (xi2 - xi1) * fi2 + (xo(k) - xi2) / (xi1 - xi2) * fi1
            enddo
        enddo

        y(k) = yin(1)
        dy(k) = (abs(y(k) - fi1) + abs(y(k) - fi2)) / 2.d0

    enddo

    return
end

! lagrange interpolation + derivative computation
subroutine lagintd(y, dery, x, x2, x3, xo, m, n, l)
    integer m, n, l, i, j, k
    real*8 x2(m, n), x3(m, n), xo(l), y(l), dery(l)
    real*8 xi(m * n), yi(m * n)
    integer x, n0, nl, nr
    real*8 xin(x), yin(x), dyin(x), xi1, xi2, fi1, fi2
    real*8 Q(x, x), dQ(x, x)

    !f2py intent(in) x, x2, x3, xo
    !f2py intent(out) y(l), dery(l)

    ! x - number of points = order + 1
    ! order of the interpolant must be <= max(m,n)
    if(x>max(m, n)) then
        x = max(m, n)
    endif

    do k = 1, l

        do i = 1, m * n
            if(m.eq.1) then
                xi(i) = x2(1, i)
                yi(i) = x3(1, i)
            else
                xi(i) = x2(i, 1)
                yi(i) = x3(i, 1)
            endif
        enddo
        !

        ! nearest nod in the grid right to xo
        do i = 1, m * n
            if(xo(k).le.xi(i)) then
                n0 = i;
                exit
            endif
        enddo
        ! number of elements left to xo
        nl = n0 - 1
        ! number of elements right to xo
        nr = m * n - n0 + 1
        !      nr = m*n - n0
        ! cut x points around xo
        if(floor(dble(x) / 2)>nl) then
            xin = xi(1:x)
            yin = yi(1:x)
        endif
        if(ceiling(dble(x) / 2)>nr) then
            xin = xi(m * n - x + 1:m * n)
            yin = yi(m * n - x + 1:m * n)
        endif
        if((floor(dble(x) / 2)<=nl).and.(ceiling(dble(x) / 2)<=nr)) then
            xin = xi(n0 - floor(dble(x) / 2):n0 + ceiling(dble(x) / 2) - 1)
            yin = yi(n0 - floor(dble(x) / 2):n0 + ceiling(dble(x) / 2) - 1)
        endif

        ! Subroutine performing the Lagrange interpolation with the
        ! Aitken method. y: interpolated value. dy: error estimated.

        ! init:
        Q(:, 1) = yin

        do i = 1, x - 1
            do j = 1, i
                xi1 = xin(i - j + 1)
                xi2 = xin(i + 1)
                fi1 = Q(i + 1, j)
                fi2 = Q(i, j)
                Q(i + 1, j + 1) = ((xo(k) - xi1) * fi1 - (xo(k) - xi2) * fi2) / (xi2 - xi1)
            enddo
        enddo

        do j = 1, x - 1
            dQ(j + 1, 2) = (Q(j + 1, 1) - Q(j, 1)) / (xin(j + 1) - xin(j))
        enddo

        do i = 2, x - 1
            do j = 2, i
                xi1 = xin(i - j + 1)
                xi2 = xin(i + 1)
                fi1 = dQ(i + 1, j)
                fi2 = dQ(i, j)
                dQ(i + 1, j + 1) = ((xo(k) - xi1) * fi1 - (xo(k) - xi2) * fi2) / (xi2 - xi1)
                fi1 = Q(i + 1, j)
                fi2 = Q(i, j)
                dQ(i + 1, j + 1) = dQ(i + 1, j + 1) + (fi1 - fi2) / (xi2 - xi1)
            enddo
        enddo

        y(k) = Q(x, x)
        dery(k) = dQ(x, x)

    enddo

    return
end


subroutine lagintt(y, dy, x, x2, x3, xo, m, n, l)
    integer m, n, l, i, j, k
    real*8 x2(m, n), x3(m, n), xo(l), y(l), dy(l)
    real*8 xi(m * n), yi(m * n)
    integer x, n0, nl, nr
    real*8 xin(x), yin(x), xi1, xi2, fi1, fi2

    !f2py intent(in) x, x2, x3, xo
    !f2py intent(out) y(l), dy(l)

    ! x - number of points = order + 1
    ! order of the interpolant must be <= max(m,n)
    if(x>max(m, n)) then
        x = max(m, n)
    endif

    do k = 1, l

        do i = 1, m * n
            if(m.eq.1) then
                xi(i) = x2(1, i)
                yi(i) = x3(1, i)
            else
                xi(i) = x2(i, 1)
                yi(i) = x3(i, 1)
            endif
        enddo
        !

        ! nearest nod in the grid right to xo
        do i = 1, m * n
            if(xo(k).le.xi(i)) then
                n0 = i;
                exit
            endif
        enddo

        ! number of points to cut from the left-hand side
        nl = floor(dble(x)) / 2
        ! number of points to cut from the right-hand side
        nr = ceiling(dble(x)) / 2
        ! check/correct bounds:
        if (size(xi(1:n0 - 1)) < nl) then
            nr = nr + nl - size(xi(1:n0 - 1))
            nl = size(xi(1:n0 - 1))
        endif
        if (size(xi(n0:m * n)) < nr) then
            nl = nl + nr - size(xi(n0:m * n))
            nr = size(xi(n0:m * n))
        endif

        ! cut the proper piece:
        xin = xi(n0 - nl:n0 + nr - 1)
        yin = yi(n0 - nl:n0 + nr - 1)


        ! Subroutine performing the Lagrange interpolation with the
        ! Aitken method. y: interpolated value. dy: error estimated.

        do  i = 1, x
            do  j = 1, x - i
                xi1 = xin(j)
                xi2 = xin(j + i)
                fi1 = yin(j)
                fi2 = yin(j + 1)
                yin(j) = (xo(k) - xi1) / (xi2 - xi1) * fi2 + (xo(k) - xi2) / (xi1 - xi2) * fi1
            enddo
        enddo

        y(k) = yin(1)
        dy(k) = (abs(y(k) - fi1) + abs(y(k) - fi2)) / 2.d0

    enddo

    return
end