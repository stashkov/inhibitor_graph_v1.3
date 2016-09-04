DROP TABLE inhibition;
CREATE TABLE inhibition
(
  id INTEGER,
  number_of_nodes TEXT,
  input_graph TEXT,
  input_matrix TEXT,
  inhibited_edges TEXT,
  in_degree TEXT,
  out_degree TEXT,
  inhibition_degree TEXT,
  inhibited_vertices TEXT,
  non_inhibited_vertices TEXT,
  known_incompatible_nodes TEXT,
  bin_of_edges TEXT,
  not_feasible TEXT,
  results TEXT,
  number_of_results INT,
  running_time REAL
);