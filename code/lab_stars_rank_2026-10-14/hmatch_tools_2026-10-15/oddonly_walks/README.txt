Odd-only walks of 15/10/2026 night (LAB), sym4g.py mode oddgap with ODDONLY=1 NOSQUARE=1, group <h> = "0,1;2,3",
warm starts og3_h_c21_NEAR_2.json (walk 1) and sq8_id_disc_c55_PSD_2.json (walk 2), 1500 s each.
WARNING: in this mode "PSD" in the log and in the file names means ONLY that the h-odd sector of T is PSD
(lambda_max of the signed odd quotient <= 3).  The even sector and U are NOT required: these structures are NOT
T, U PSD four-star blocks.  Purpose: test whether the odd bound can be tight (eigenvalue 3) without a grid.
Result: no.  The gap 3 - lambda_max went down to 3.1e-6 (oddonly_2_NEAR_8.json, exact det(3I - Gamma^odd) = 81 != 0),
and no structure with an odd eigenvalue 3 was found (no _ODD_ file).
