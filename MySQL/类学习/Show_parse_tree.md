- [Show\_parse\_tree](#show_parse_tree)


# Show_parse_tree
class Show_parse_tree {
  private:
    std::vector<Json_object*, std::allocator<Json_object*> > m_json_obj_stack;
    Json_object_ptr m_root_obj;
    Show_parse_tree *m_parent_show_parse_tree;
    const char *m_reference_pos;
    static const Show_parse_tree::Parse_tree_comparator m_comparator;

    bool make_child(Json_object *);
    Json_object * pop_json_object(void);
  public:
    Show_parse_tree(Show_parse_tree *);
    bool push_level(const POS &, const char *);
    Json_object * get_current_parent(void);
    std::string get_parse_tree(void);
    bool pop_level(void);
}
