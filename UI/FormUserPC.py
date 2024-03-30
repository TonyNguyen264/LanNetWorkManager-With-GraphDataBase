import tkinter as tk
from tkinter import ttk
from neo4j import GraphDatabase
import ipaddress
import re

# from SignIn_SignUp import get_user_role
# root = tk.Tk()
# root.configure(bg="#313131")
#
# root.title("Forest")


driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "tony0101tony"))

list_ip_avaiable = []
list_ip_range = []
list_data_treeview = []
# list_network_dbs=[]
# list_netmask_dbs=[]
# list_maphong_dbs=[]

network_sw = []
# usernameDN = ''
# roleDN = ''


def show_form_admin(usernameDN, roleDN):
    # Biến để lưu trữ giá trị của Entry
    # bỏ . để sort ip
    def custom_sort_key(item):
        ip = item['ip'].replace('.', '')  # Loại bỏ dấu chấm khỏi địa chỉ IP
        return int(ip)




    # load toàn bộ switch layer
    def load_switchlayer(combobox):
        with driver.session() as session:
            query = "MATCH (n:swl) RETURN n.name AS swl ORDER BY n.ipaddress"
            result = session.run(query)
            list_swl = [record["swl"] for record in result]
            if 'switch layer server' in list_swl:
                list_swl.remove('switch layer server')
            combobox["values"] = list_swl

    # load switch có liên kết với switch layer đã chọn
    def load_relate_switch(event):
        selected_swl = combobox_swl.get()

        # driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "tony0101tony"))
        with driver.session() as session:
            query = "MATCH (c:swl{name: $name})-[:switched]->(n:sw) RETURN n.name AS sw ORDER BY n.ip"
            result = session.run(query, name=selected_swl)
            sw = [record["sw"] for record in result]
            combobox_switch["values"] = sw

    # load data pc từ switch đã chọn
    def load_data(event):
        treeview.delete(*treeview.get_children())
        # print("-------------------------------------------------------------------------------------")
        global list_data_treeview
        # print(list_data_treeview)
        global list_ip_range
        list_ip_range.clear()
        global list_ip_avaiable
        # list_ip_avaiable.clear()
        global network_sw


        list_ip_range.clear()

        list_ip_pc_sw = []
        list_pc = []
        get_name_sw = combobox_switch.get()
        # lấy dữ liệu từ dbs
        with driver.session() as session:
            query = "MATCH (c:sw{name:$name})-[:connected_to]->(n:pc)-[:belongs_to]->(a) " \
                    "RETURN n.mapc as mapc, n.name AS name, n.ipaddress AS ip, n.network AS network," \
                    " n.netmask AS netmask,a.maphong as room ORDER BY n.ipaddress"
            result = session.run(query, name=get_name_sw)
            # result = sorted(result, key=lambda x: x[:0])
            for record in result:
                list_pc.append(
                    {"mapc": record["mapc"], "name": record["name"], 'ip': record["ip"], 'netmask': record["netmask"],
                     'network': record["network"], 'room': record["room"]})


        list_pc = sorted(list_pc, key=custom_sort_key)
        for pc in list_pc:
            treeview.insert("", "end", values=(
                pc["mapc"], pc["name"], pc["ip"], pc["netmask"], pc["network"], pc["room"]))
            list_ip_pc_sw.append(pc["ip"])
            if pc["network"] not in network_sw:
                network_sw.append(pc["network"])

        list_ip_range = calculate_ip_ranges(network_sw)  # tính ip range

        ip_start = []
        for i in list_ip_range:
            ip_start.append(i[0])
        combobox_ip_range_start['value'] = ip_start  # đổ ip vào cmb

        for ip_range in list_ip_range:
            for ip in ip_range:
                if ip not in list_ip_pc_sw:
                    list_ip_avaiable.append(ip)



    def toggle_mode():  # chuyển chế độ sáng tối
        if mode_switch.instate(["selected"]):
            style.theme_use("forest-light")
            # root(bg="white")
            root.configure(bg="white")
            treeFrame.pack_propagate(False)

            # root.resizable(False, False)
        else:
            style.theme_use("forest-dark")
            root.configure(bg="#313131")
            treeFrame.pack_propagate(False)

    # tính ip range
    def calculate_ip_ranges(networks):
        ip_ranges = []
        for network in networks:
            network_obj = ipaddress.IPv4Network(network, strict=False)
            ip_range = [str(ip) for ip in network_obj.hosts()]
            # ip=[]
            # ip.append(ip_range[0])
            # ip.append(ip_range[-1])
            ip_ranges.append(ip_range)
        return ip_ranges

    def calculate_subnet_mask(network):
        # Tách phần địa chỉ network từ network (e.g., '172.16.1.32/27' -> '172.16.1.32')
        network_address = network.split('/')[0]

        # Chuyển phần địa chỉ network thành các thành phần số
        octets = network_address.split('.')
        octet_values = [int(octet) for octet in octets]

        # Tính subnet mask dựa trên độ dài của subnet (được chỉ định bởi phần sau dấu / trong network)
        subnet_mask_length = int(network.split('/')[1])
        subnet_mask_octets = [0] * 4
        for i in range(subnet_mask_length):
            subnet_mask_octets[i // 8] |= 1 << (7 - i % 8)

        # Định dạng subnet mask thành chuỗi dạng dấu chấm

        subnet_mask_parts = [str(octet) for octet in subnet_mask_octets]

        subnet_mask = ".".join(subnet_mask_parts)
        return subnet_mask

    # tính ip end khi có ip đầu
    def load_ip_range_end(event):
        global list_ip_range
        selected_ip = combobox_ip_range_start.get()
        # print('load_ip_range_end', list_ip_range)
        for ip in list_ip_range:
            if ip[0] == selected_ip:
                strvar_ip_end.set(ip[-1])

    # tự fill vào entry khi clik vào bảng
    def on_edit_selected(event):
        selected_item = treeview.focus()

        if selected_item:
            mapc, name, ip, netmask, network, room = treeview.item(selected_item)["values"]
            strvar_mapc.set(mapc)
            strvar_name.set(name)
            strvar_ip.set(ip)
            strvar_subnetmask.set(netmask)
            strvar_network.set(network)
            strvar_maphong.set(room)

    # click vào tạo ac chuyển qua trang tạo acc


    # click vào tạo đoi mk chuyển qua trang đổi mk
    def button_change_pass():
        import ChangePass
        ChangePass.signup_command(usernameDN)



    def refesh_data():  # giống load data nhưng k có sự kiện
        treeview.delete(*treeview.get_children())
        # print("-------------------------------------------------------------------------------------")
        global list_data_treeview
        global list_ip_range
        list_ip_range.clear()
        global list_ip_avaiable
        # list_ip_avaiable.clear()
        global network_sw
        # network_sw.clear()


        list_ip_range.clear()

        list_ip_pc_sw = []
        list_pc = []
        get_name_sw = combobox_switch.get()
        # lấy dữ liệu từ dbs
        with driver.session() as session:
            query = "MATCH (c:sw{name:$name})-[:connected_to]->(n:pc)-[:belongs_to]->(a) " \
                    "RETURN n.mapc as mapc, n.name AS name, n.ipaddress AS ip, n.network AS network," \
                    " n.netmask AS netmask,a.maphong as room ORDER BY n.ipaddress"
            result = session.run(query, name=get_name_sw)
            # result = sorted(result, key=lambda x: x[:0])
            for record in result:
                list_pc.append(
                    {"mapc": record["mapc"], "name": record["name"], 'ip': record["ip"], 'netmask': record["netmask"],
                     'network': record["network"], 'room': record["room"]})
                # print(record)
                # print(list_pc)
        # print(list_pc)
        # sắp xếp data theo ip
        # print(list_pc)
        # sắp xếp data theo ip
        list_pc = sorted(list_pc, key=custom_sort_key)
        for pc in list_pc:
            treeview.insert("", "end", values=(
                pc["mapc"], pc["name"], pc["ip"], pc["netmask"], pc["network"], pc["room"]))
            list_ip_pc_sw.append(pc["ip"])
            if pc["network"] not in network_sw:
                network_sw.append(pc["network"])
        #     print(pc)
        # print(network_sw)
        # list_ip_range=[]
        # print('network_sw lần 2', network_sw)
        list_ip_range = calculate_ip_ranges(network_sw)  # tính ip range
        # print(list_ip_range)

        # ip=[]
        # ip.append(ip_range[0])
        # ip.append(ip_range[-1])
        ip_start = []
        for i in list_ip_range:
            ip_start.append(i[0])
        combobox_ip_range_start['value'] = ip_start  # đổ ip vào cmb
        # combobox_ip_avaiable['value']=[]
        # combobox_ip_avaiable['value'] = list_ip_avaiable

        #     strvar_ip_end.set(list_ip[-1])
        #     list_ip=[str(list_ip) if isinstance(value, ipaddress.IPv4Address) else value for value in list_ip]

        for ip_range in list_ip_range:
            for ip in ip_range:
                if ip not in list_ip_pc_sw:
                    list_ip_avaiable.append(ip)


        # list_data_treeview.clear()
        # lấy dữ liệu bảng vào list để so sánh khi add và edit
        # for item_id in treeview.get_children():
        #     values = treeview.item(item_id)["values"]
        #     list_data_treeview.append(values)





    def on_network_change(*args):
        network = entry_network.get()
        if validate_network_format(network):
            strvar_subnetmask.set(calculate_subnet_mask(network))
        else:
            strvar_subnetmask.set('subnetmask')

    def on_maphong_change(*args):
        maphong = entry_maphong.get()
        l_phong = []
        with driver.session() as session:
            result = session.run(
                "match(n:room{maphong:$maphong}) return n.maphong as maphong,n.name as name, n.location as location, n.roomtype as roomtype",
                maphong=maphong)
            for record in result:
                l_phong.append({"maphong": record["maphong"], "name": record["name"], "location": record["location"],
                                "roomtype": record["roomtype"]})
        if l_phong == []:
            strvar_room_info.set("room info")
        else:
            room_info = 'Maphong: ' + str(l_phong[0]["maphong"]) + '      |      Name: ' + str(
                l_phong[0]["name"]) + '      |      ' + 'Location: ' + str(
                l_phong[0]["location"]) + '      |      ' + 'roomtype: ' + str(l_phong[0]["roomtype"])
            strvar_room_info.set(room_info)
            # print('count: ', room_info)

        # strvar_room_info.set(""l_phong["maphong"])

    # def get_network(combobox):
    #     global network_sw
    #     combobox["values"] = network_sw





    def validate_network_format(network_str):
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,2}$'
        if re.match(pattern, network_str):
            return True
        return False


    def Logout():
        import SignIn_SignUp
        root.destroy()  # Đóng cửa sổ chính
        SignIn_SignUp.show_login()
        # paned.pack_propagate(False)

    def button_view_switch():
        import FormUserSwitch
        driver.close()
        FormUserSwitch.show_form_user_sw(usernameDN, roleDN, root)

    # def toggle_mode():
    #     if switch.instate(["selected"]):
    #         style.theme_use("forest-light")
    #     else:
    #         style.theme_use("forest-dark")

    # Create a style
    # root = tk.Tk()
    # tạo giao diện
    root = tk.Tk()
    root.option_add("*tearOff", False)  # This is always a good idea
    strvar_mapc=tk.StringVar()
    strvar_name=tk.StringVar()
    strvar_ip=tk.StringVar()
    strvar_network = tk.StringVar()
    strvar_subnetmask = tk.StringVar()
    strvar_ip_end = tk.StringVar()
    strvar_maphong = tk.StringVar()
    strvar_room_info = tk.StringVar()

    strvar_mapc.set("Mapc")
    strvar_name.set("Name")
    strvar_ip.set("Ip")
    strvar_network.set("Network")
    strvar_subnetmask.set("Netmask")
    strvar_maphong.set("Maphong")



    strvar_network.trace("w", on_network_change)
    strvar_maphong.trace("w", on_maphong_change)

    # Make the app responsive
    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=1)

    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    # root.geometry('10x+180+150')
    style.theme_use("forest-dark")

    # Create a Frame for the Checkbuttons
    Accout_frame = ttk.LabelFrame(root, text="Account", padding=(20, 10))
    Accout_frame.grid(row=0, rowspan=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
    Accout_frame.columnconfigure(index=0, weight=1)
    Accout_frame.configure()

    # Checkbuttons

    # print(username)
    label = ttk.Label(Accout_frame, text="Username: ")
    label.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="ew")
    entry = ttk.Entry(Accout_frame)
    entry.insert(0, usernameDN)
    entry.configure(state="readonly")
    entry.grid(row=1, column=0, padx=5, pady=(0, 10), sticky="ew")

    label_1 = ttk.Label(Accout_frame, text="Role: ")
    label_1.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")
    entry_1 = ttk.Entry(Accout_frame)
    entry_1.insert(0, roleDN)
    entry_1.configure(state="readonly")
    entry_1.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

    button = ttk.Button(Accout_frame, text="Change Password", command=button_change_pass)
    button.grid(row=4, column=0, padx=5, pady=10, sticky="nsew")


    button_2 = ttk.Button(Accout_frame, text="Logout", command=Logout)
    button_2.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")
    # Separator
    # separator = ttk.Separator(root)
    # separator.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")

    # Create a Frame for the Radiobuttons
    Mode_frame = ttk.LabelFrame(root, text="Change Dark Mode", padding=(20, 10))
    Mode_frame.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="nsew")
    Mode_frame.columnconfigure(index=0, weight=1)
    # Radiobuttons

    # Switch
    # Togglebutton
    # toggle_var = tk.IntVar(value=0)  # 0: OFF, 1: ON
    # button = ttk.Checkbutton(Mode_frame, variable=toggle_var, text="Dark Mode", style="ToggleButton",command=toggle_mode())
    # button.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

    mode_switch = ttk.Checkbutton(
        Mode_frame, text="Mode", style="Switch", command=toggle_mode)
    mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

    # Create a Frame for input widgets
    widgets_frame = ttk.LabelFrame(root, text="Input", padding=(0, 0, 0, 10))
    widgets_frame.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nsew", rowspan=4)
    widgets_frame.columnconfigure(index=0, weight=1)
    # widgets_frame.configure(width=50)
    # widgets_frame.pack_propagate(False)

    combobox_swl = ttk.Combobox(widgets_frame, state="readonly")
    # combobox_swl.current(0)
    combobox_swl.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="ew", columnspan=2)
    combobox_swl.set("choose switch layer")
    combobox_swl.bind("<<ComboboxSelected>>", load_relate_switch)

    # separator = ttk.Separator(widgets_frame)
    # separator.grid(row=6, column=0, padx=(20, 10), pady=10, sticky="ew")

    combobox_switch = ttk.Combobox(widgets_frame, state="readonly")
    combobox_switch.set("choose switch")
    combobox_switch.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
    combobox_switch.bind("<<ComboboxSelected>>", load_data)

    load_switchlayer(combobox_swl)

    separator = ttk.Separator(widgets_frame)
    separator.grid(row=2, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")

    entry_MaPC = ttk.Entry(widgets_frame,state="readonly",textvariable=strvar_mapc)
    entry_MaPC.insert(0, "MaPC")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_MaPC.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    entry_name = ttk.Entry(widgets_frame,state="readonly",textvariable=strvar_name)
    entry_name.insert(0, "Name")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_name.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    entry_ip = ttk.Entry(widgets_frame,state="readonly",textvariable=strvar_ip)
    entry_ip.insert(0, "IP")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_ip.grid(row=5, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    # combobox_ip = ttk.Combobox(widgets_frame, state="readonly")
    # combobox_ip.set("choose ip")
    # combobox_ip.grid(row=4, column=0, padx=5, pady=5, sticky="ew",columnspan=2)
    # get_subnetmask(combobox_S)

    entry_subnetmask = ttk.Entry(widgets_frame, textvariable=strvar_subnetmask,state="readonly")
    entry_subnetmask.insert(0, "subnetmask")
    entry_subnetmask.configure(state="readonly")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_subnetmask.grid(row=6, column=0, padx=5, pady=5, sticky="ew", columnspan=2)


    entry_network = ttk.Entry(widgets_frame, textvariable=strvar_network,state="readonly")
    entry_network.insert(0, "network")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_network.grid(row=7, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

    separator = ttk.Separator(widgets_frame)
    separator.grid(row=8, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")

    entry_maphong = ttk.Entry(widgets_frame, textvariable=strvar_maphong,state="readonly")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_maphong.grid(row=9, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

    #

    separator = ttk.Separator(widgets_frame)
    separator.grid(row=10, column=0, padx=(20, 10), pady=10, sticky="ew")
    # Button
    button_load = ttk.Button(widgets_frame, text="load", command=refesh_data)
    button_load.grid(row=11, column=0, padx=5, pady=5, sticky="ew")

    button_switch_mode = ttk.Button(widgets_frame, text="view switch", command=button_view_switch)
    button_switch_mode.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Panedwindow
    paned = ttk.PanedWindow(root)
    paned.grid(row=0, column=2, pady=(20, 10), sticky="nsew", rowspan=4)
    paned.configure(width=800)

    # Pane #1
    pane_1 = ttk.Frame(paned)
    paned.add(pane_1, weight=10)

    # Create a Frame for the Treeview
    treeFrame = ttk.Frame(pane_1)
    treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

    # Scrollbar
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")

    # Treeview
    # treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2), height=12)
    # treeScroll.config(command=treeview.yview)

    # treeFrame = ttk.Frame(frame)
    # treeFrame.grid(row=0, column=1, pady=10)
    # treeScroll = ttk.Scrollbar(treeFrame)
    # treeScroll.pack(side="right", fill="y")

    cols = ("MaPC", "Name", "IP", "Subnetmask", "Network", "Room")
    treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=15)
    treeview.column("MaPC", width=50)
    treeview.column("Name", width=150)
    treeview.column("IP", width=90)
    treeview.column("Subnetmask", width=100)
    treeview.column("Network", width=100)
    treeview.column("Room", width=100)

    cols = ("MaPC", "Name", "IP", "Subnetmask", "Network", "Room")

    for col_name in cols:
        treeview.heading(col_name, text=col_name, anchor="w")
    treeview.bind("<<TreeviewSelect>>", on_edit_selected)
    treeview.pack(expand=True, fill="both")

    # Pane #2
    pane_2 = ttk.Frame(paned)
    paned.add(pane_2, weight=1)
    # pane_2.configure(height=90)
    # pane_2.pack_propagate(False)
    # pane_2.pack(expand=True, side="bottom", ipady=10)

    # Notebook
    notebook = ttk.Notebook(pane_2)

    # tab 0
    tab_0 = ttk.Frame(notebook)
    tab_0.columnconfigure(index=0, weight=1)
    tab_0.columnconfigure(index=1, weight=1)
    tab_0.rowconfigure(index=0, weight=1)
    tab_0.rowconfigure(index=1, weight=1)
    notebook.add(tab_0, text="Room Info")

    entry_room_info = ttk.Entry(tab_0, textvariable=strvar_room_info)
    # entry_room_info.insert(0, 'Room Info')
    entry_room_info.configure(state="readonly")
    entry_room_info.grid(row=0, column=0, padx=5, pady=(0, 10), columnspan=2, sticky="nsew")
    # Tab #1
    tab_1 = ttk.Frame(notebook)
    tab_1.columnconfigure(index=0, weight=1)
    tab_1.columnconfigure(index=1, weight=1)
    # tab_1.rowconfigure(index=0, weight=1)
    # tab_1.rowconfigure(index=1, weight=1)
    notebook.add(tab_1, text="IP Range")

    # Label
    # label = ttk.Label(tab_1, text="Forest ttk theme", justify="center")
    # label.grid(row=1, column=0, pady=10, columnspan=2)

    # entry_ipr_start = ttk.Entry(tab_1, textvariable=strvar_ip_start)
    # entry_ipr_start.configure(state="readonly")
    # entry_ipr_start.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="nsew")

    combobox_ip_range_start = ttk.Combobox(tab_1, state="readonly")
    combobox_ip_range_start.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="nsew")
    combobox_ip_range_start.set("choose ip start")
    combobox_ip_range_start.bind("<<ComboboxSelected>>", load_ip_range_end)

    # separator = ttk.Separator(tab_1,text="|")
    # separator.grid(row=0, column=1,  padx=5, pady=(0, 10), sticky="ew")
    #
    entry_ipr_end = ttk.Entry(tab_1, textvariable=strvar_ip_end)
    entry_ipr_end.insert(0, 'ip range end')
    entry_ipr_end.configure(state="readonly")
    entry_ipr_end.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="nsew")


    notebook.pack(expand=True, fill="both", padx=5, pady=5)

    # Sizegrip

    # Center the window, and set minsize

    # Start the main loop
    # root.mainloop()
    # show_form_user("tony","admin")
    root.mainloop()
    driver.close()

# #
# if __name__ == "__main__":
#     show_form_admin("tonyuser", 'user')
