select
	s_name,
	s_address
from
	supplier,
	nation
where
	s_suppkey in (
		select
			ps_suppkey
		from
			partsupp
		where
			ps_partkey in (
				select
					p_partkey
				from
					part
				where
					p_name like 'lime%'
			)
			and ps_availqty > (
				select
					0.5 * sum(l_quantity)
				from
					lineitem
				where
					l_partkey = ps_partkey
					and l_suppkey = ps_suppkey
					and l_shipdate >= '1994-01-01'
					and l_shipdate < date_add( '1994-01-01' ,interval '1' year)
			)
	)
	and s_nationkey = n_nationkey
	and n_name = 'MOZAMBIQUE'
order by
	s_name;

