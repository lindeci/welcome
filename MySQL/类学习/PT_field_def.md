class PT_field_def : public PT_field_def_base {
  private:
    Mem_root_array<PT_column_attr_base*> *opt_attrs;

  public:
    PT_field_def(const POS &, PT_type *, Mem_root_array<PT_column_attr_base*> *);
    virtual bool do_contextualize(context_t *);
}