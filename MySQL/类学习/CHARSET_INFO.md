```cpp
struct CHARSET_INFO {
    unsigned int number;
    unsigned int primary_number;
    unsigned int binary_number;
    unsigned int state;
    const char *csname;
    const char *m_coll_name;
    const char *comment;
    const char *tailoring;
    Coll_param *coll_param;
    const uint8_t *ctype;
    const uint8_t *to_lower;
    const uint8_t *to_upper;
    const uint8_t *sort_order;
    MY_UCA_INFO *uca;
    const uint16_t *tab_to_uni;
    const MY_UNI_IDX *tab_from_uni;
    const MY_UNICASE_INFO *caseinfo;
    const lex_state_maps_st *state_maps;
    const uint8_t *ident_map;
    unsigned int strxfrm_multiply;
    uint8_t caseup_multiply;
    uint8_t casedn_multiply;
    unsigned int mbminlen;
    unsigned int mbmaxlen;
    unsigned int mbmaxlenlen;
    my_wc_t min_sort_char;
    my_wc_t max_sort_char;
    uint8_t pad_char;
    bool escape_with_backslash_is_dangerous;
    uint8_t levels_for_compare;
    MY_CHARSET_HANDLER *cset;
    MY_COLLATION_HANDLER *coll;
    Pad_attribute pad_attribute;
}
```