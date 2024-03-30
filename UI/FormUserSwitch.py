import tkinter as tk
from tkinter import ttk
import openpyxl
from tkinter import ttk
from neo4j import GraphDatabase
import ipaddress
from tkinter import messagebox
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

network_sw = []
usernameDN = ''
roleDN = ''


def show_form_user_sw(usernameDN, roleDN, log):
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

    # load data pc từ switch đã chọn
    def load_data(event):
        treeview.delete(*treeview.get_children())
        # print("-------------------------------------------------------------------------------------")
        global list_ip_range
        list_ip_range.clear()
        global list_ip_avaiable
        # list_ip_avaiable.clear()
        global network_sw

        list_ip_pc_sw = []

        # list_ip_avaiable.clear()
        list_ip_range.clear()

        list_pc = []
        get_name_swl = combobox_swl.get()
        # lấy dữ liệu từ dbs
        with driver.session() as session:
            query = "MATCH (c:swl{name:$name})-[:switched]->(n) " \
                    "RETURN n.masw as masw, n.name as name, " \
                    "n.ipaddress as ip,n.network as network, n.netmask as netmask order by n.ipaddress"
            result = session.run(query, name=get_name_swl)
            # result = sorted(result, key=lambda x: x[:0])
            for record in result:
                list_pc.append(
                    {"masw": record["masw"], "name": record["name"], 'ip': record["ip"], 'netmask': record["netmask"],
                     'network': record["network"]})
                # print(record)
                # print(list_pc)
        # print(list_pc)
        # sắp xếp data theo ip
        list_pc = sorted(list_pc, key=custom_sort_key)
        for pc in list_pc:
            treeview.insert("", "end", values=(
                pc["masw"], pc["name"], pc["ip"], pc["netmask"], pc["network"]))
            list_ip_pc_sw.append(pc["ip"])
            if pc["network"] not in network_sw:
                network_sw.append(pc["network"])  # lấy ra network của pc để tính ip range và ip khả dụng
        # print('network:' ,network_sw)
        #     print(pc)
        # print(network_sw)
        # list_ip_range=[]
        # print('network_sw lần 2', network_sw)
        list_ip_range = calculate_ip_ranges(network_sw)  # tính ip range
        # print(list_ip_range)
        # ip=[]
        # ip.append(ip_range[0])
        # ip.append(ip_range[-1])

        strvar_ip_start.set(list_pc[0]['ip'])
        strvar_ip_end.set(list_ip_range[0][-1])

        for ip_range in list_ip_range:
            for ip in ip_range:
                if ip not in list_ip_pc_sw:
                    list_ip_avaiable.append(ip)

        list_data_treeview.clear()
        # lấy dữ liệu bảng vào list để so sánh khi add và edit
        for item_id in treeview.get_children():
            values = treeview.item(item_id)["values"]
            list_data_treeview.append(values)

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

    # tính ip end khi có ip đầu

    # tự fill vào entry khi clik vào bảng
    def on_edit_selected(event):
        selected_item = treeview.focus()
        if selected_item:
            masw, name, ip, netmask, network = treeview.item(selected_item)["values"]

            strvar_masw.set(masw)
            strvar_name.set(name)
            strvar_ip.set(ip)
            strvar_network.set(network)
            strvar_subnetmask.set(netmask)

            # strvar_subnetmask.set(netmask)

    # click vào tạo ac chuyển qua trang tạo acc

    # click vào tạo đoi mk chuyển qua trang đổi mk
    def button_change_pass():
        import ChangePass
        ChangePass.signup_command(usernameDN)

    def refesh_data():  # giống load data nhưng k có sự kiện
        treeview.delete(*treeview.get_children())
        # print("-------------------------------------------------------------------------------------")
        global list_ip_range
        list_ip_range.clear()
        global list_ip_avaiable
        # list_ip_avaiable.clear()
        global network_sw
        # network_sw.clear()

        # print('list_ip_avaiable lần 1', list_ip_avaiable)
        # print(' list_ip_range lần 1', list_ip_range)
        list_ip_pc_sw = []

        # list_ip_avaiable.clear()
        list_ip_range.clear()

        list_ip_pc_sw = []
        list_pc = []
        get_name_swl = combobox_swl.get()
        # lấy dữ liệu từ dbs
        with driver.session() as session:
            query = "MATCH (c:swl{name:$name})-[:switched]->(n) " \
                    "RETURN n.masw as masw, n.name as name, " \
                    "n.ipaddress as ip,n.network as network, n.netmask as netmask order by n.ipaddress"
            result = session.run(query, name=get_name_swl)
            # result = sorted(result, key=lambda x: x[:0])
            for record in result:
                list_pc.append(
                    {"masw": record["masw"], "name": record["name"], 'ip': record["ip"], 'netmask': record["netmask"],
                     'network': record["network"]})
                # print(record)
                # print(list_pc)
        # print(list_pc)
        # sắp xếp data theo ip
        list_pc = sorted(list_pc, key=custom_sort_key)
        for pc in list_pc:
            treeview.insert("", "end", values=(
                pc["masw"], pc["name"], pc["ip"], pc["netmask"], pc["network"]))
            list_ip_pc_sw.append(pc["ip"])
            if pc["network"] not in network_sw:
                network_sw.append(pc["network"])  # lấy ra network của pc để tính ip range và ip khả dụng

        list_ip_range = calculate_ip_ranges(network_sw)  # tính ip range

        strvar_ip_start.set(list_pc[0]['ip'])
        strvar_ip_end.set(list_ip_range[0][-1])

        for ip_range in list_ip_range:
            for ip in ip_range:
                if ip not in list_ip_pc_sw:
                    list_ip_avaiable.append(ip)

        list_data_treeview.clear()
        # lấy dữ liệu bảng vào list để so sánh khi add và edit
        for item_id in treeview.get_children():
            values = treeview.item(item_id)["values"]
            list_data_treeview.append(values)

    def button_view_pc():
        log.deiconify()
        root.destroy()
        # import FormAdminSwitch
        # FormAdminSwitch.show_form_admin_switch(usernameDN,roleDN,root)


    root = tk.Toplevel(log)
    root.option_add("*tearOff", False)  # This is always a good idea
    strvar_masw = tk.StringVar()
    strvar_name = tk.StringVar()
    strvar_ip = tk.StringVar()
    strvar_network = tk.StringVar()
    strvar_subnetmask = tk.StringVar()
    strvar_ip_start = tk.StringVar()
    strvar_ip_end = tk.StringVar()

    root.columnconfigure(index=0, weight=1)
    root.columnconfigure(index=1, weight=1)
    root.columnconfigure(index=2, weight=1)
    root.rowconfigure(index=0, weight=1)
    root.rowconfigure(index=1, weight=1)
    root.rowconfigure(index=2, weight=1)

    style = ttk.Style(root)
    # root.tk.call("source", "forest-light.tcl")
    # root.tk.call("source", "forest-dark.tcl")
    # root.geometry('10x+180+150')
    style.theme_use("forest-dark")

    # Create a Frame for the Checkbuttons
    Accout_frame = ttk.LabelFrame(root, text="Account", padding=(20, 10))
    Accout_frame.grid(row=0, rowspan=3, column=0, padx=(20, 10), pady=(20, 10), sticky="nsew")
    Accout_frame.columnconfigure(index=0, weight=1)

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

    # separator = ttk.Separator(root)
    # separator.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")

    # Create a Frame for the Radiobuttons
    Mode_frame = ttk.LabelFrame(root, text="Change Dark Mode", padding=(20, 10))
    Mode_frame.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="nsew")
    Mode_frame.columnconfigure(index=0, weight=1)
    # Radiobuttons

    # Switch

    mode_switch = ttk.Checkbutton(
        Mode_frame, text="Mode", style="Switch", command=toggle_mode)
    mode_switch.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

    # Create a Frame for input widgets
    widgets_frame = ttk.LabelFrame(root, text="Input", padding=(0, 0, 0, 10))
    widgets_frame.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nsew", rowspan=4)
    widgets_frame.columnconfigure(index=0, weight=1)

    combobox_swl = ttk.Combobox(widgets_frame, state="readonly")
    # combobox_swl.current(0)
    combobox_swl.grid(row=0, column=0, padx=5, pady=(5, 5), sticky="ew", columnspan=2)
    combobox_swl.set("choose switch layer")
    combobox_swl.bind("<<ComboboxSelected>>", load_data)

    # separator = ttk.Separator(widgets_frame)
    # separator.grid(row=6, column=0, padx=(20, 10), pady=10, sticky="ew")
    load_switchlayer(combobox_swl)

    entry_masw = ttk.Entry(widgets_frame, state='readonly', textvariable=strvar_masw)
    entry_masw.insert(0, "masw")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_masw.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    entry_name = ttk.Entry(widgets_frame, state='readonly', textvariable=strvar_name)
    entry_name.insert(0, "Name")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_name.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    entry_ip = ttk.Entry(widgets_frame, state='readonly', textvariable=strvar_ip)
    entry_ip.insert(0, "IP")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_ip.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew", columnspan=2)

    # combobox_ip = ttk.Combobox(widgets_frame, state="readonly")
    # combobox_ip.set("choose ip")
    # combobox_ip.grid(row=4, column=0, padx=5, pady=5, sticky="ew",columnspan=2)
    # get_subnetmask(combobox_S)

    entry_subnetmask = ttk.Entry(widgets_frame, state="readonly", textvariable=strvar_subnetmask)
    entry_subnetmask.insert(0, "subnetmask")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_subnetmask.grid(row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

    entry_network = ttk.Entry(widgets_frame, textvariable=strvar_network, state='readonly')
    entry_network.insert(0, "network")
    # name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
    entry_network.grid(row=6, column=0, padx=5, pady=5, sticky="ew", columnspan=2)

    separator = ttk.Separator(widgets_frame)
    separator.grid(row=7, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")

    button_load = ttk.Button(widgets_frame, text="load", command=refesh_data)
    button_load.grid(row=8, column=0, padx=5, pady=5, sticky="ew")

    separator = ttk.Separator(widgets_frame)
    separator.grid(row=10, column=0, columnspan=2, padx=(20, 10), pady=10, sticky="ew")

    button_switch_mode = ttk.Button(widgets_frame, text="view pc", command=button_view_pc)
    button_switch_mode.grid(row=11, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

    # Panedwindow
    paned = ttk.PanedWindow(root)
    paned.grid(row=0, column=2, pady=(20, 10), sticky="nsew", rowspan=4)

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

    cols = ("masw", "Name", "IP", "Subnetmask", "Network")
    treeview = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=15)
    treeview.column("masw", width=50)
    treeview.column("Name", width=150)
    treeview.column("IP", width=90)
    treeview.column("Subnetmask", width=100)
    treeview.column("Network", width=100)
    cols = ("masw", "Name", "IP", "Subnetmask", "Network")

    for col_name in cols:
        treeview.heading(col_name, text=col_name, anchor="w")
    treeview.bind("<<TreeviewSelect>>", on_edit_selected)
    treeview.pack(expand=True, fill="both")

    # Pane #2
    pane_2 = ttk.Frame(paned)
    paned.add(pane_2, weight=1)
    # pane_2.pack(expand=True, side="bottom", ipady=10)

    # Notebook
    notebook = ttk.Notebook(pane_2)

    # Tab #1
    tab_1 = ttk.Frame(notebook)
    tab_1.columnconfigure(index=0, weight=1)
    tab_1.columnconfigure(index=1, weight=1)
    tab_1.rowconfigure(index=0, weight=1)
    tab_1.rowconfigure(index=1, weight=1)
    notebook.add(tab_1, text="IP Range")

    # Label
    # label = ttk.Label(tab_1, text="Forest ttk theme", justify="center")
    # label.grid(row=1, column=0, pady=10, columnspan=2)

    # entry_ipr_start = ttk.Entry(tab_1, textvariable=strvar_ip_start)
    # entry_ipr_start.configure(state="readonly")
    # entry_ipr_start.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="nsew")

    # combobox_ip_range_start = ttk.Combobox(tab_1, state="readonly")
    # combobox_ip_range_start.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="nsew")
    # combobox_ip_range_start.set("choose ip start")
    # combobox_ip_range_start.bind("<<ComboboxSelected>>", load_ip_range_end)

    entry_ipr_start = ttk.Entry(tab_1, textvariable=strvar_ip_start)
    entry_ipr_start.configure(state="readonly")
    entry_ipr_start.grid(row=0, column=0, padx=5, pady=(0, 10), sticky="nsew")

    # separator = ttk.Separator(tab_1,text="|")
    # separator.grid(row=0, column=1,  padx=5, pady=(0, 10), sticky="ew")
    #
    entry_ipr_end = ttk.Entry(tab_1, textvariable=strvar_ip_end)
    entry_ipr_end.configure(state="readonly")
    entry_ipr_end.grid(row=0, column=1, padx=5, pady=(0, 10), sticky="nsew")

    notebook.pack(expand=True, fill="both", padx=5, pady=5)

    # Sizegrip

    # Center the window, and set minsize

    # Start the main loop
    # root.mainloop()
    # show_form_user("tony","admin")
    log.withdraw()
    driver.close()

# if __name__ == "__main__":
# show_form_user_pc("tony", 'admin')
