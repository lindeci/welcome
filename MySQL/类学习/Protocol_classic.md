- [Protocol\_classic](#protocol_classic)
- [Protocol](#protocol)

# Protocol_classic
```cpp
class Protocol_classic : public Protocol {
  private:
    ulong m_client_capabilities; /**< 客户端能力 */

  protected:
    THD *m_thd; /**< 线程处理数据 */
    String *packet; /**< 数据包 */
    String convert; /**< 转换字符串 */
    uint field_pos; /**< 字段位置 */
    bool send_metadata; /**< 发送元数据标志 */
    enum_field_types *field_types; /**< 字段类型枚举 */
    uint count; /**< 计数 */
    uint field_count; /**< 字段数量 */
    uint sending_flags; /**< 发送标志 */
    ulong input_packet_length; /**< 输入数据包长度 */
    uchar *input_raw_packet; /**< 输入的原始数据包 */
    const CHARSET_INFO *result_cs; /**< 结果字符集 */

  public:
    bool bad_packet; /**< 无效数据包标志 */

    Protocol_classic(void); /**< 构造函数 */
    Protocol_classic(THD *); /**< 带 THD 参数的构造函数 */

  private:
    bool parse_packet(COM_DATA *, enum_server_command); /**< 解析数据包 */
    bool net_store_data_with_conversion(const uchar *, size_t, const CHARSET_INFO *, const CHARSET_INFO *); /**< 存储经过转换的数据 */

  protected:
    virtual bool send_ok(uint, uint, ulonglong, ulonglong, const char *); /**< 发送 OK 数据包 */
    virtual bool send_eof(uint, uint); /**< 发送 EOF 数据包 */
    virtual bool send_error(uint, const char *, const char *); /**< 发送错误数据包 */
    virtual bool store_ps_status(ulong, uint, uint, ulong); /**< 存储预处理状态 */

  public:
    void init(THD *); /**< 初始化 */
    virtual bool store_field(const Field *); /**< 存储字段 */
    virtual bool store_string(const char *, size_t, const CHARSET_INFO *); /**< 存储字符串 */
    virtual int read_packet(void); /**< 读取数据包 */
    virtual int get_command(COM_DATA *, enum_server_command *); /**< 获取命令 */
    bool create_command(COM_DATA *, enum_server_command, uchar *, size_t); /**< 创建命令 */
    virtual bool flush(void); /**< 刷新数据 */
    virtual void end_partial_result_set(void); /**< 结束部分结果集 */
    virtual bool end_row(void); /**< 结束行 */
    virtual uint get_rw_status(void); /**< 获取读写状态 */
    virtual bool get_compression(void); /**< 获取压缩状态 */
    virtual char *get_compression_algorithm(void); /**< 获取压缩算法 */
    virtual uint get_compression_level(void); /**< 获取压缩级别 */
    virtual bool start_result_metadata(uint, uint, const CHARSET_INFO *); /**< 开始结果元数据 */
    virtual bool end_result_metadata(void); /**< 结束结果元数据 */
    virtual bool send_field_metadata(Send_field *, const CHARSET_INFO *); /**< 发送字段元数据 */
    virtual void abort_row(void); /**< 中止行 */
    virtual enum_vio_type connection_type(void) const; /**< 连接类型 */
    my_socket get_socket(void); /**< 获取套接字 */
    bool init_net(Vio *); /**< 初始化网络 */
    void claim_memory_ownership(bool); /**< 拥有内存所有权 */
    void end_net(void); /**< 结束网络 */
    bool write(const uchar *, size_t); /**< 写入数据 */
    uchar get_error(void); /**< 获取错误 */
    void set_max_packet_size(ulong); /**< 设置最大数据包大小 */
    virtual int shutdown(bool); /**< 关闭 */
    void wipe_net(void); /**< 清除网络 */
    virtual bool connection_alive(void) const; /**< 连接是否存活 */
    virtual ulong get_client_capabilities(void); /**< 获取客户端能力 */
    void set_client_capabilities(ulong); /**< 设置客户端能力 */
    void add_client_capability(ulong); /**< 添加客户端能力 */
    void remove_client_capability(unsigned long); /**< 移除客户端能力 */
    virtual bool has_client_capability(unsigned long); /**< 是否有指定的客户端能力 */
    NET *get_net(void); /**< 获取网络 */
    Vio *get_vio(void); /**< 获取 Vio */
    const Vio *get_vio(void) const; /**< 获取 Vio，常版本 */
    void set_vio(Vio *); /**< 设置 Vio */
    void set_output_pkt_nr(uint); /**< 设置输出数据包编号 */
    uint get_output_pkt_nr(void); /**< 获取输出数据包编号 */
    String *get_output_packet(void); /**< 获取输出数据包 */
    ulong get_packet_length(void); /**< 获取数据包长度 */
    uchar *get_raw_packet(void); /**< 获取原始数据包 */
    virtual void set_read_timeout(ulong, bool); /**< 设置读取超时 */
    virtual void set_write_timeout(ulong); /**< 设置写入超时 */
    void set_result_character_set(const CHARSET_INFO *); /**< 设置结果字符集 */
}
```

# Protocol
```cpp
class Protocol {
  private:
    Protocol *m_previous_protocol; /**< 前一个协议 */

  public:
    ~Protocol(); /**< 析构函数 */
    Protocol *pop_protocol(void); /**< 弹出协议 */
    void push_protocol(Protocol *); /**< 推入协议 */
    virtual int read_packet(void); /**< 读取数据包 */
    virtual int get_command(COM_DATA *, enum_server_command *); /**< 获取命令 */
    virtual Protocol::enum_protocol_type type(void) const; /**< 协议类型 */
    virtual enum_vio_type connection_type(void) const; /**< 连接类型 */
    virtual bool store_null(void); /**< 存储空值 */
    virtual bool store_tiny(longlong, uint32); /**< 存储超小整数 */
    bool store_tiny(longlong); /**< 存储超小整数 */
    virtual bool store_short(longlong, uint32); /**< 存储短整数 */
    bool store_short(longlong); /**< 存储短整数 */
    virtual bool store_long(longlong, uint32); /**< 存储长整数 */
    bool store_long(longlong); /**< 存储长整数 */
    virtual bool store_longlong(longlong, bool, uint32); /**< 存储长长整数 */
    bool store_longlong(longlong, bool); /**< 存储长长整数 */
    virtual bool store_decimal(const my_decimal *, uint, uint); /**< 存储十进制数 */
    virtual bool store_string(const char *, size_t, const CHARSET_INFO *); /**< 存储字符串 */
    virtual bool store_float(float, uint32, uint32); /**< 存储单精度浮点数 */
    virtual bool store_double(double, uint32, uint32); /**< 存储双精度浮点数 */
    virtual bool store_datetime(const MYSQL_TIME &, uint); /**< 存储日期时间 */
    virtual bool store_date(const MYSQL_TIME &); /**< 存储日期 */
    virtual bool store_time(const MYSQL_TIME &, uint); /**< 存储时间 */
    virtual bool store_field(const Field *); /**< 存储字段 */
    bool store(int); /**< 存储整数 */
    bool store(uint32); /**< 存储无符号整数 */
    bool store(longlong); /**< 存储长整数 */
    bool store(ulonglong); /**< 存储长长整数 */
    bool store(const char *, const CHARSET_INFO *); /**< 存储字符串 */
    bool store(String *); /**< 存储字符串对象 */
    bool store(const LEX_STRING &, const CHARSET_INFO *); /**< 存储 LEX_STRING 对象 */
    virtual ulong get_client_capabilities(void); /**< 获取客户端能力 */
    virtual bool has_client_capability(unsigned long); /**< 是否有指定的客户端能力 */
    virtual bool connection_alive(void) const; /**< 连接是否存活 */
    virtual void start_row(void); /**< 开始行 */
    virtual bool end_row(void); /**< 结束行 */
    virtual void abort_row(void); /**< 中止行 */
    virtual void end_partial_result_set(void); /**< 结束部分结果集 */
    virtual int shutdown(bool); /**< 关闭连接 */
    virtual uint get_rw_status(void); /**< 获取读写状态 */
    virtual bool get_compression(void); /**< 获取压缩状态 */
    virtual char *get_compression_algorithm(void); /**< 获取压缩算法 */
    virtual uint get_compression_level(void); /**< 获取压缩级别 */
    virtual bool start_result_metadata(uint, uint, const CHARSET_INFO *); /**< 开始结果元数据 */
    virtual bool send_field_metadata(Send_field *, const CHARSET_INFO *); /**< 发送字段元数据 */
    virtual bool end_result_metadata(void); /**< 结束结果元数据 */
    virtual bool send_ok(uint, uint, ulonglong, ulonglong, const char *); /**< 发送 OK 数据包 */
    virtual bool send_eof(uint, uint); /**< 发送 EOF 数据包 */
    virtual bool send_error(uint, const char *, const char *); /**< 发送错误数据包 */
    virtual bool flush(void); /**< 刷新数据 */
    virtual bool store_ps_status(ulong, uint, uint, ulong); /**< 存储预处理状态 */
    virtual bool send_parameters(List<Item_param> *, bool); /**< 发送参数 */
}

```